class Weapon(object):

    def __init__(self, name, mt, hit, wt, crit):
        self.name = name
        self.might = mt
        self.hit = hit
        self.weight = wt
        self.crit = crit


class IronWeapon(Weapon):

    def __init__(self, name):
        Weapon.__init__(self, name, 0, 90, 0, 0)


class IronLance(IronWeapon):

    def __init__(self):
        IronWeapon.__init__(self, 'Iron Lance')


class IronAxe(IronWeapon):

    def __init__(self):
        IronWeapon.__init__(self, 'Iron Axe')


class IronSword(IronWeapon):

    def __init__(self):
        IronWeapon.__init__(self, 'Iron Sword')


class DevilAxe(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Devil Axe', 15, 70, 5, 5)
