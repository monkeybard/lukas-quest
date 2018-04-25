import numpy as np
from lukas_quest.weapons import *


class FEClass:
    """Base class to represent an FE Class."""
    def __init__(self, name=None, promotions=None, base_stats=None, base_growths=None, default_weapon=None):
        self.name = name
        self.promotions = promotions
        self.base_stats = np.array(base_stats)
        self.base_growths = np.array(base_growths)
        self.default_weapon = default_weapon


class Baron (FEClass):

    def __init__(self):
        FEClass.__init__(self, 'Baron', set(), [40, 22, 6, 4, 0, 18, 7], [5, 5, 0, -10, -5, 5, 0], IronLance())


class Knight (FEClass):

    def __init__(self):
        FEClass.__init__(self, 'Knight', {Baron()}, [34, 16, 2, 2, 0, 12, 1], [5, 5, 0, -10, -5, 5, 0], IronLance())


class Soldier (FEClass):

    def __init__(self):
        FEClass.__init__(self, 'Soldier', {Knight()}, [26, 10, 1, 3, 0, 5, 0], [5, 5, 0, -10, -5, 5, 0], IronLance())


class Brigand (FEClass):

    def __init__(self):
        FEClass.__init__(self, 'Brigand', set(), [26, 7, 1, 2, 0, 2, 0], [120, 45, 40, 45, 0, 40, 10], IronAxe())
