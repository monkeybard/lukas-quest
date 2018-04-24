import pickle
import numpy
import random
from collections import Counter
from lukas_quest.classes import *

filepath = './lukas_quest/lukas.save'
default_feclass = Soldier()
default_level = 2
default_exp = 0
default_stats = numpy.array([22, 10, 4, 4, 2, 5, 2])
default_stat_caps = numpy.array([52, 40, 40, 38, 40, 42, 40])
default_growth_rates = numpy.array([50, 30, 40, 25, 30, 45, 20])
default_stamina = 500
default_happiness = 0
default_inventory = Counter()
default_steps = 0


class Lukas(object):
    """
    Stores information on Lukas himself.
    """

    @staticmethod
    def stat_name_to_index(name):
        return {'HP': 0, 'ATK': 1, 'SKL': 2, 'SPD': 3, 'LCK': 4, 'DEF': 5, 'RES': 6}[name.upper()]

    def __init__(self, other=None):
        try:
            self.load(other)
        except OSError:
            print("No file found, resetting...")
            self.feclass = default_feclass
            self.level = default_level
            self.exp = default_exp
            self.stats = default_stats
            self.current_hp = self.stats[(Lukas.stat_name_to_index('HP'))]
            self.stat_caps = default_stat_caps
            self.growth_rates = default_growth_rates
            self.stamina = default_stamina
            self.happiness = default_happiness
            self.inventory = default_inventory
            self.steps = default_steps

    def copy(self, other):
        check = dir(other)
        self.feclass = other.feclass if 'feclass' in check else default_feclass
        self.level = other.level if 'level' in check else default_level
        self.exp = other.exp if 'exp' in check else default_exp
        self.stats = other.stats if 'stats' in check else default_stats
        self.current_hp = other.current_hp if 'current_hp' in check else\
                                                                        self.stats[(Lukas.stat_name_to_index('HP'))]
        self.stat_caps = other.stat_caps if 'stat_caps' in check else default_stat_caps
        self.growth_rates = other.growth_rates if 'growth_rates' in check else default_growth_rates
        self.stamina = other.stamina if 'stamina' in check else default_stamina
        self.happiness = other.happiness if 'happiness' in check else default_happiness
        self.inventory = other.inventory if 'inventory' in check else default_inventory
        self.steps = other.steps if 'steps' in check else default_steps

    def load(self, other=None):
        if other is None:
            print("Loading from file...")
            with open(filepath, 'rb') as to_load:
                loaded = pickle.load(to_load)
                self.copy(loaded)
        else:
            print("Copying existing Lukas...")
            self.copy(other)

    def save(self):
        with open(filepath, 'wb+') as save_to:
            pickle.dump(self, save_to)

    def reset(self):
        self.feclass = default_feclass
        self.level = default_level
        self.exp = default_exp
        self.stats = default_stats
        self.current_hp = self.stats[(Lukas.stat_name_to_index('HP'))]
        self.stat_caps = default_stat_caps
        self.growth_rates = default_growth_rates
        self.stamina = default_stamina
        self.happiness = default_happiness
        self.inventory = default_inventory
        self.steps = default_steps

    def give_exp(self, exp):
        """Awards exp. Returns true if level up occurred."""
        if self.level < 20:
            self.exp += exp
            while self.exp >= 100:
                self.levelup()
                if self.level == 20:
                    self.exp = 0
                else:
                    self.exp -= 100
                return True
        return False

    def adjust_stamina(self, stamina):
        """Change stamina by value specified."""
        self.stamina = min(max(0, self.stamina + int(stamina)), 500)

    def adjust_happiness(self, happiness):
        """Change happiness by value specified."""
        self.happiness = min(max(0, self.happiness + int(happiness)), 500)

    def adjust_hp(self, hp):
        """Change HP by value specified. Returns True if Lukas died and reset."""
        self.current_hp = min(self.current_hp + int(hp), self.stats[Lukas.stat_name_to_index('HP')])
        if self.current_hp <= 0:
            self.reset()
            return True
        return False

    def levelup(self):
        if self.level != 20:
            current_growths = self.growth_rates + self.feclass.base_growths
            for i in range(len(self.stats)):
                self.increase_stat(i, increase_by=current_growths[i]//100)
                if random.randrange(100)+1 <= (current_growths[i] % 100):
                    self.increase_stat(i)
            self.level += 1

    def increase_stat(self, stat_index, increase_by=1):
        old_stat = self.stats[stat_index]
        self.stats[stat_index] = min(self.stats[stat_index] + increase_by, self.stat_caps[stat_index])
        return self.stats[stat_index] - old_stat

    def class_change(self, new_class):
        self.feclass = new_class
        self.level = 1
        self.exp = 0
        self.stats = numpy.maximum(self.stats, self.feclass.base_stats)
