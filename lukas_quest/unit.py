import numpy
import random
from lukas_quest.classes import *
from lukas_quest.config import *


def stat_name_to_index(name):
    return {'HP': 0, 'ATK': 1, 'SKL': 2, 'SPD': 3, 'LCK': 4, 'DEF': 5, 'RES': 6}[name.upper()]


class Unit(object):

    def __init__(self, name, feclass, level, stats, stat_caps, growth_rates=[0]*7):
        self.name = name
        self.feclass = feclass
        self.weapon = feclass.default_weapon
        self.level = level
        self.stats = numpy.array(stats)
        self.current_hp = self.stats[stat_name_to_index('HP')]
        self.stat_caps = numpy.array(stat_caps)
        self.growth_rates = numpy.array(growth_rates)

    def adjust_hp(self, hp):
        """Change HP by value specified. Returns True if hp has hit 0 and reset."""
        self.current_hp = min(self.current_hp + int(hp), self.stats[stat_name_to_index('HP')])
        if self.current_hp <= 0:
            return True
        return False

    def levelup(self):
        increased = np.array([0] * 7)
        if self.level != 20:
            current_growths = self.growth_rates + self.feclass.base_growths
            for i in range(len(self.stats)):
                # %growths > 100 are guaranteed stat increases + (growth % 100)% chance of increasing further
                increased[i] += self.increase_stat(i, increase_by=current_growths[i]//100)
                if random.randrange(100)+1 <= (current_growths[i] % 100):
                    increased[i] += self.increase_stat(i)
            self.level += 1
        return increased

    def increase_stat(self, stat_index, increase_by=1):
        old_stat = self.stats[stat_index]
        self.stats[stat_index] = min(self.stats[stat_index] + increase_by, self.stat_caps[stat_index])
        return self.stats[stat_index] - old_stat

    def equip(self, new_weapon):
        self.weapon = new_weapon

    @property
    def combat_stats(self):
        u_atk = self.stats[stat_name_to_index('ATK')] + self.weapon.might
        u_def = self.stats[stat_name_to_index('DEF')]
        u_atkspd = max(0, self.stats[stat_name_to_index('SPD')] - self.weapon.weight)
        u_hit = self.stats[stat_name_to_index('SKL')] + self.weapon.hit
        u_avoid = u_atkspd * 2
        u_crit = (self.stats[stat_name_to_index('SKL')] // 2) + self.weapon.crit
        u_critavoid = self.stats[stat_name_to_index('LCK')]
        return u_atk, u_def, u_atkspd, u_hit, u_avoid, u_crit, u_critavoid


class Enemy(Unit):
    """
    Simple container for an enemy.
    """
    def __init__(self, name=None, feclass=Brigand(),
                 level=1, base_stats=None, drops=[], drop_dist=[], is_boss=False):
        """By default, a level 1 Brigand."""
        Unit.__init__(self, name if name else feclass.name, feclass,
                      1, base_stats if base_stats else feclass.base_stats, [52, 40, 40, 40, 40, 40, 40])
        self.drops = drops
        self.drop_dist = drop_dist
        self.is_boss = is_boss
        self.autolevel(level)

    def autolevel(self, level):
        for i in range(level-1):
            self.levelup()
        self.current_hp = self.stats[stat_name_to_index('HP')]


class Player(Unit):
    """
    Stores information on Lukas himself.
    """

    def __init__(self):
        Unit.__init__(self, player_name,
                      default_feclass, default_level, default_stats, default_stat_caps, default_growth_rates)
        self.exp = default_exp
        self.stamina = default_stamina
        self.happiness = default_happiness
        self.inventory = default_inventory
        self.steps = default_steps

    def reset(self):
        self.name = player_name
        self.feclass = default_feclass
        self.level = default_level
        self.exp = default_exp
        self.stats = default_stats
        self.current_hp = self.stats[stat_name_to_index('HP')]
        self.stat_caps = default_stat_caps
        self.growth_rates = default_growth_rates
        self.stamina = default_stamina
        self.happiness = default_happiness
        self.inventory = default_inventory
        self.steps = default_steps

    def give_exp(self, exp):
        """Awards exp. Returns a table of stat increases if level up occurred."""
        if self.level < 20:
            self.exp += exp
            while self.exp >= 100:
                increased = self.levelup()
                if self.level == 20:
                    self.exp = 0
                else:
                    self.exp -= 100
                return increased
            return np.array([0]*7)
        return None

    def adjust_stamina(self, stamina):
        """Change stamina by value specified."""
        self.stamina = min(max(0, self.stamina + int(stamina)), 500)

    def adjust_happiness(self, happiness):
        """Change happiness by value specified."""
        self.happiness = min(max(0, self.happiness + int(happiness)), 500)

    def class_change(self, new_class):
        self.feclass = new_class
        self.level = 1
        self.exp = 0
        self.stats = numpy.maximum(self.stats, self.feclass.base_stats)

    @property
    def combat_stats(self):
        p_atk, p_def, p_atkspd, p_hit, p_avoid, p_crit, p_critavoid = Unit.combat_stats.fget(self)
        happiness_factor = self.happiness//50
        return p_atk, p_def, p_atkspd, p_hit, p_avoid + happiness_factor, p_crit + happiness_factor, p_critavoid
