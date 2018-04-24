import numpy
import copy
import random
from collections import deque
from lukas_quest import items
from lukas_quest.lukas import Lukas
from lukas_quest.unit import Unit
from lukas_quest.classes import *


class Quest(object):
    """
    Provides functionality to interact with Lukas.
    """

    class Enemy(Unit):
        """
        Simple container for an enemy.
        """
        def __init__(self, name='Brigand', feclass=Brigand(), level=1):
            self.name = name
            Unit.__init__(self, feclass, 1, feclass.base_stats, [52, 40, 40, 40, 40, 40, 40])
            self.autolevel(level)

        def autolevel(self, level):
            for i in range(level-1):
                self.levelup()
            self.current_hp = self.stats[Unit.stat_name_to_index('HP')]

    def __init__(self):
        self._lukas = Lukas()
        self.in_battle = False
        self._enemy = Quest.Enemy()
        self.quest_log = deque()

    def battle_status(in_battle):
        def wrap(fun):
            def wrap_f(self, *args, **kwargs):
                if self.in_battle == in_battle:
                    return fun(self, *args, **kwargs)
                else:
                    self.quest_log.appendleft("You cannot do that out of battle." if in_battle
                                              else "You cannot do that in battle.")
            return wrap_f
        return wrap

    @property
    def status(self):
        return copy.deepcopy(self._lukas)

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
                max_level = self._lukas.steps//10
                self._enemy = Quest.Enemy(level=max(1, random.randrange(max_level-3, max_level)))
                self.quest_log.appendleft("{} appeared!".format(self._enemy.name))
                self.in_battle = True

            if self._lukas.steps % 20 == 0 or self._lukas.steps % 30 == 0:
                numpy.random.choice([find_item, get_exp, trigger_battle], size=1, p=[0.6, 0.1, 0.3])[0]()

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
            'n' if item_name[0] in ['a', 'e', 'i', 'o', 'u'] else '', items.clean_name(item_name)))

    @battle_status(False)
    def use(self, item_name):
        """Use an item in the inventory."""
        if self._lukas.inventory[item_name]:
            item = getattr(items, item_name)
            self.quest_log.appendleft("Used a{} {}.".format(
                'n' if item_name[0] in ['a', 'e', 'i', 'o', 'u'] else '', items.clean_name(item_name)))
            item(self._lukas, self.quest_log)
            self._lukas.inventory[item_name] -= 1
        else:
            self.quest_log.appendleft("You do not have {}.".format(items.clean_name(item_name)))

    @battle_status(False)
    def get_promotion_list(self):
        return list(self._lukas.feclass.promotions)

    @battle_status(False)
    def class_change(self, new_class):
        self._lukas.class_change(new_class)
        self.quest_log.appendleft("Lukas has changed class to {}.".format(new_class.name))

    @battle_status(True)
    def resolve_phase(self):
        l_at, l_de, l_as, l_h, l_a, l_c, l_ca, e_at, e_de, e_as, e_h, e_a, e_c, e_ca = self.battle_stats()

        def take_turn(defender, attack, hit, crit, defense, avoid, critavoid):
            accuracy = max(0, hit - avoid)
            crit_rate = max(0, crit - critavoid)
            damage = max(0, attack - defense)
            if random.randrange(100)+1 <= accuracy:
                if random.randrange(100)+1 <= crit_rate:
                    self.quest_log.appendleft("Critical Hit! {} damage!".format(damage*3))
                    result = defender.adjust_hp(-damage*3)
                else:
                    self.quest_log.appendleft("Hit! {} damage.".format(damage))
                    result = defender.adjust_hp(-damage)
                return result
            else:
                self.quest_log.appendleft("Miss!")
                return False

        def victory():
            self.in_battle = False
            self.quest_log.appendleft("Lukas has won the battle!")
            if self._enemy.feclass.name == 'Brigand':
                self.give(numpy.random.choice(['drinking_water', 'hard_bread', 'sweet_cookie'], 1,
                                              [0.3, 0.5, 0.2])[0])
                self.process_exp(30)
                self._lukas.adjust_happiness(30)

        def defeat():
            self.in_battle = False
            self.quest_log.appendleft("Lukas has lost the battle...")
            self._lukas.adjust_happiness(-30)
            self._lukas.steps = max(0, self._lukas.steps - 100)
            self._lukas.stamina = 0

        def lukas_turn():
            self.quest_log.appendleft("Lukas attacks!")
            if take_turn(self._enemy, l_at, l_h, l_c, e_de, e_a, e_ca):
                victory()
                return True
            return False

        def enemy_turn():
            self.quest_log.appendleft("{} attacks!".format(self._enemy.feclass.name))
            if take_turn(self._lukas, e_at, e_h, e_c, l_de, l_a, l_ca):
                defeat()
                return True
            return False

        if lukas_turn():
            return
        if enemy_turn():
            return
        if l_as > e_as:
            lukas_turn()
        elif e_as > l_as:
            enemy_turn()

    @battle_status(True)
    def flee(self):
        self.in_battle = False
        self._lukas.steps = max(0, self._lukas.steps - 50)
        self.quest_log.appendleft("Lukas has fled the battle.")
        if self._enemy.current_hp < self._enemy.stats[Unit.stat_name_to_index('HP')]:
            self.process_exp(10)

    @battle_status(True)
    def enemy_status(self):
        return copy.deepcopy(self._enemy)

    @battle_status(True)
    def battle_stats(self):
        lukas_atk = self._lukas.stats[Unit.stat_name_to_index('ATK')]
        lukas_def = self._lukas.stats[Unit.stat_name_to_index('DEF')]
        lukas_atkspd = self._lukas.stats[Unit.stat_name_to_index('SPD')]
        lukas_hit = self._lukas.stats[Unit.stat_name_to_index('SKL')] + 90
        lukas_avoid = lukas_atkspd * 2
        lukas_crit = self._lukas.stats[Unit.stat_name_to_index('SKL')] // 2
        lukas_critavoid = self._lukas.stats[Unit.stat_name_to_index('LCK')]
        enemy_atk = self._enemy.stats[Unit.stat_name_to_index('ATK')]
        enemy_def = self._enemy.stats[Unit.stat_name_to_index('DEF')]
        enemy_atkspd = self._enemy.stats[Unit.stat_name_to_index('SPD')]
        enemy_hit = self._enemy.stats[Unit.stat_name_to_index('SKL')] + 90
        enemy_avoid = enemy_atkspd * 2
        enemy_crit = self._enemy.stats[Unit.stat_name_to_index('SKL')] // 2
        enemy_critavoid = self._enemy.stats[Unit.stat_name_to_index('LCK')]
        return lukas_atk, lukas_def, lukas_atkspd, lukas_hit, lukas_avoid, lukas_crit, lukas_critavoid, \
               enemy_atk, enemy_def, enemy_atkspd, enemy_hit, enemy_avoid, enemy_crit, enemy_critavoid
