import lukas_quest.items
from collections import deque
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

    def use(self, item):
        if self._lukas.inventory[item]:
            died, effect_string = item(self._lukas)
            if not died:
                self._lukas.inventory[item] -= 1

    def get_promotion_list(self):
        return self._lukas.feclass.promotions

    def class_change(self, new_class):
        self._lukas.class_change(new_class)
