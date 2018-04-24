from collections import deque
from lukas_quest import items
from lukas_quest.lukas import *


class Quest(object):
    """
    Provides functionality to interact with Lukas.
    """

    def __init__(self):
        self._lukas = Lukas()
        self.quest_log = deque

    @property
    def status(self):
        return Lukas(other=self._lukas)

    def save(self):
        self._lukas.save()

    def step(self):
        """Moves Lukas 1 step forward, may trigger an event."""
        self._lukas.steps += 1

    def get_inventory(self):
        return self._lukas.inventory

    def give(self, item_name):
        self._lukas.inventory[item_name] += 1

    def use(self, item_name):
        if self._lukas.inventory[item_name]:
            item = getattr(items, item_name)
            effect_string = item(self._lukas)
            self._lukas.inventory[item_name] -= 1
            return effect_string

    def get_promotion_list(self):
        return list(self._lukas.feclass.promotions)

    def class_change(self, new_class):
        self._lukas.class_change(new_class)
