import numpy
import random
from lukas_quest.classes import *


class Unit(object):

    @staticmethod
    def stat_name_to_index(name):
        return {'HP': 0, 'ATK': 1, 'SKL': 2, 'SPD': 3, 'LCK': 4, 'DEF': 5, 'RES': 6}[name.upper()]

    def __init__(self, feclass, level, stats, stat_caps, growth_rates=[0,0,0,0,0,0,0]):
        self.feclass = feclass
        self.level = level
        self.stats = numpy.array(stats)
        self.current_hp = self.stats[Unit.stat_name_to_index('HP')]
        self.stat_caps = numpy.array(stat_caps)
        self.growth_rates = numpy.array(growth_rates)

    def adjust_hp(self, hp):
        """Change HP by value specified. Returns True if hp has hit 0 and reset."""
        self.current_hp = min(self.current_hp + int(hp), self.stats[Unit.stat_name_to_index('HP')])
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
