import numpy
from collections import deque
from lukas_quest import items
from lukas_quest.lukas import Lukas
from lukas_quest.unit import Unit


class Quest(object):
    """
    Provides functionality to interact with Lukas.
    """

    class Enemy(Unit):
        """
        Simple container for an enemy.
        """
        def __init__(self, name, feclass, level, base_stats, stat_caps):
            self.name = name
            Unit.__init__(self, feclass, level, base_stats, stat_caps)
            self.autolevel()

        def autolevel(self):
            for i in range(self.level-1):
                self.levelup()

    def __init__(self):
        self._lukas = Lukas()
        self._in_battle = False
        self._enemy = numpy.array([])
        self.quest_log = deque()

    def battle_status(in_battle):
        def wrap(fun):
            def wrap_f(self, *args, **kwargs):
                return fun(self, *args, **kwargs) if self._in_battle == in_battle else None
            return wrap_f
        return wrap

    @property
    def status(self):
        return Lukas(other=self._lukas)

    @battle_status(False)
    def save(self):
        self._lukas.save()

    @battle_status(False)
    def step(self):
        """Moves Lukas 1 step forward, may trigger an event."""
        if self._lukas.stamina > 0:
            self._lukas.steps += 1
            self._lukas.adjust_stamina(-1)

            # define possible events
            def find_item():
                food_dist = [0.7/18]*16 + [0.25/10]*10 + [0.7/18]*2 + [0.05/7]*7
                random_food = numpy.random.choice(items.foods, size=1, p=food_dist)[0]
                self.give(random_food)

            def get_exp():
                exp = numpy.random.choice([10, 15, 25, 50, 100], size=1, p=[0.5, 0.25, 0.125, 0.1, 0.025])[0]
                self.process_exp(exp)

            def trigger_battle():
                self.quest_log.appendleft("An enemy approaches.")

            if self._lukas.steps % 20 == 0 or self._lukas.steps % 30 == 0:
                numpy.random.choice([find_item, get_exp, trigger_battle], size=1, p=[0.0, 1.0, 0.0])[0]()

            if self._lukas.stamina == 0:
                self.quest_log.appendleft("Lukas: I'm afraid... I can walk no further...")

    def get_inventory(self):
        return self._lukas.inventory

    @battle_status(False)
    def process_exp(self, exp):
        result = self._lukas.give_exp(exp)
        if result is not None:
            self.quest_log.appendleft("Got {} EXP.".format(exp))
            if any(result):
                # levelled up
                self.quest_log.appendleft("Levelled up!")
                self.quest_log.appendleft(self._lukas.stats)

    @battle_status(False)
    def give(self, item_name):
        """Adds an item to the inventory."""
        self._lukas.inventory[item_name] += 1
        self.quest_log.appendleft("Obtained a{} {}.".format(
            'n' if item_name[0] in ['a', 'e', 'i', 'o', 'u'] else '', item_name.replace('_', ' ').title()))

    @battle_status(False)
    def use(self, item_name):
        """Use an item in the inventory."""
        if self._lukas.inventory[item_name]:
            item = getattr(items, item_name)
            item(self._lukas, self.quest_log)
            self._lukas.inventory[item_name] -= 1

    @battle_status(False)
    def get_promotion_list(self):
        return list(self._lukas.feclass.promotions)

    @battle_status(False)
    def class_change(self, new_class):
        self._lukas.class_change(new_class)
        self.quest_log.appendleft("Lukas has changed class to {}.".format(new_class.name))

    @battle_status(True)
    def resolve_phase(self):
        pass

    @battle_status(True)
    def flee(self):
        pass

    @battle_status(True)
    @property
    def enemy_status(self):
        pass

    @battle_status(True)
    @property
    def battle_forecast(self):
        pass
