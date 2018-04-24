import pickle
import numpy
import random
from collections import Counter
from lukas_quest.classes import *
from lukas_quest.unit import Unit

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


class Lukas(Unit):
    """
    Stores information on Lukas himself.
    """

    def __init__(self, other=None):
        try:
            self.load(other)
        except OSError:
            print("No file found, resetting...")
            Unit.__init__(self, default_feclass, default_level, default_stats, default_stat_caps, default_growth_rates)
            self.exp = default_exp
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
                                                                        self.stats[(Unit.stat_name_to_index('HP'))]
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
        self.current_hp = self.stats[(Unit.stat_name_to_index('HP'))]
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
