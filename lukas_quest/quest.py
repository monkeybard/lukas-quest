import copy
import pickle
from collections import deque
from lukas_quest.config import *
from lukas_quest import items
from lukas_quest.unit import *

loading_debug = True


class Quest(object):
    """
    Provides functionality to interact with player.
    """

    def __init__(self):
        try:
            self.load()
        except OSError:
            global loading_debug
            if loading_debug:
                print("No file found, resetting...")
            self._player = Player()
            self._enemy = Enemy()
            self.in_battle = False
            self.quest_log = deque()
        loading_debug = False

    def copy(self, other):
        """Copies other into self with default values if not found."""
        check = dir(other)
        self._player = other._player if '_player' in check else Player()
        self._enemy = other._enemy if '_enemy' in check else Enemy()
        self.in_battle = other.in_battle if 'in_battle' in check else False
        self.quest_log = other.quest_log if 'quest_log' in check else deque()

    def load(self, other=None):
        global loading_debug
        if other is None:
            if loading_debug:
                print("Loading from file...")
            with open(filepath, 'rb') as to_load:
                loaded = pickle.load(to_load)
                # use copy so old saves can still work if more fields are added
                self.copy(loaded)
        else:
            if loading_debug:
                print("Copying existing quest...")
            self.copy(other)

    def save(self):
        with open(filepath, 'wb+') as save_to:
            pickle.dump(self, save_to)

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
        return copy.deepcopy(self._player)

    @battle_status(False)
    def step(self):
        """Moves player 1 step forward, may trigger an event."""
        if self._player.stamina > 0:
            self._player.steps += 1
            self._player.adjust_stamina(-1)

            if self._player.stamina == 0:
                self.quest_log.appendleft(out_of_stamina)

            # define possible events
            def find_item():
                random_food = numpy.random.choice(item_drops, size=1, p=item_dist)[0]
                self.give(random_food)

            def get_exp():
                exp = numpy.random.choice(exp_drops, size=1, p=exp_dist)[0]
                self.process_exp(exp)

            def trigger_battle():
                max_level = self._player.steps//enemy_level_increase_interval
                e_level = max(1, random.randrange(max_level-enemy_level_variance, max_level))
                map_stage = list(
                    sorted([stage_number for stage_number in enemy_map if self._player.steps > stage_number]))[-1]
                e_class, e_weapons, e_drop_table = enemy_map[map_stage][0][
                    numpy.random.choice(range(len(enemy_map[map_stage][0])), 1, enemy_map[map_stage][1])[0]]
                self._enemy = Enemy(feclass=e_class, level=e_level, drops=e_drop_table[0], drop_dist=e_drop_table[1])
                self._enemy.equip(numpy.random.choice(e_weapons[0], 1, e_weapons[1])[0])
                self.quest_log.appendleft("{} appeared!".format(self._enemy.name))
                self.in_battle = True

            if self._player.steps in boss_map:
                # trigger boss fight
                boss_class, boss_name, boss_weapon, boss_level, boss_bases, drop_table = boss_map[self._player.steps]
                self._enemy = Enemy(boss_name, boss_class, boss_level, boss_bases, drop_table[0], drop_table[1], True)
                self._enemy.equip(boss_weapon)
                self.quest_log.appendleft("Boss {} appeared!".format(self._enemy.name))
                self.in_battle = True
            else:
                if any([self._player.steps % interval == 0 for interval in event_intervals]):
                    numpy.random.choice([find_item, get_exp, trigger_battle], size=1, p=event_dist)[0]()

    def get_inventory(self):
        return self._player.inventory

    @battle_status(False)
    def process_exp(self, exp):
        result = self._player.give_exp(exp)
        if result is not None:
            self.quest_log.appendleft("Got {} EXP.".format(exp))
            if any(result):
                # levelled up
                self.quest_log.appendleft("Levelled up!")
                self.quest_log.appendleft(self._player.stats)

    @battle_status(False)
    def give(self, item_name):
        """Adds an item to the inventory."""
        self._player.inventory[item_name] += 1
        self.quest_log.appendleft("Obtained a{} {}.".format(
            'n' if item_name[0] in ['a', 'e', 'i', 'o', 'u'] else '', items.clean_name(item_name)))

    @battle_status(False)
    def use(self, item_name):
        """Use an item in the inventory."""
        if self._player.inventory[item_name]:
            item = getattr(items, item_name)
            self.quest_log.appendleft("Used a{} {}.".format(
                'n' if item_name[0] in ['a', 'e', 'i', 'o', 'u'] else '', items.clean_name(item_name)))
            item(self._player, self.quest_log)
            self._player.inventory[item_name] -= 1
        else:
            self.quest_log.appendleft("You do not have {}.".format(items.clean_name(item_name)))

    @battle_status(False)
    def get_promotion_list(self):
        return list(self._player.feclass.promotions)

    @battle_status(False)
    def class_change(self, new_class):
        self._player.class_change(new_class)
        self.quest_log.appendleft("{} has changed class to {}.".format(self._player.name, new_class.name))

    @battle_status(True)
    def resolve_phase(self):
        (l_at, l_de, l_as, l_h, l_a, l_c, l_ca), (e_at, e_de, e_as, e_h, e_a, e_c, e_ca) = self.battle_stats()

        def take_turn(attacker_name, defender, attack, hit, crit, defense, avoid, critavoid):
            self.quest_log.appendleft("{} attacks!".format(attacker_name))
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
            self.quest_log.appendleft("{} has won the battle!".format(self._player.name))
            if self._enemy.drops:
                self.give(numpy.random.choice(self._enemy.drops, 1, self._enemy.drop_dist)[0])
            if self._enemy.is_boss:
                self.process_exp(100)
                self._player.adjust_happiness(100)
            else:
                self.process_exp(30)
                self._player.adjust_happiness(30)

        def defeat():
            self.in_battle = False
            self.quest_log.appendleft("{} has lost the battle...".format(self._player.name))
            self._player.adjust_happiness(death_happiness_penalty)
            self._player.steps = max(0, self._player.steps + death_steps_penalty)
            self._player.stamina = 0

        def player_turn():
            if take_turn(self._player.name, self._enemy, l_at, l_h, l_c, e_de, e_a, e_ca):
                victory()
                return True
            return False

        def enemy_turn():
            if take_turn(self._enemy.name, self._player, e_at, e_h, e_c, l_de, l_a, l_ca):
                defeat()
                return True
            return False

        if player_turn():
            return
        if enemy_turn():
            return
        if l_as > e_as:
            player_turn()
        elif e_as > l_as:
            enemy_turn()

    @battle_status(True)
    def flee(self):
        self.in_battle = False
        self._player.adjust_happiness(flee_happiness_penalty)
        self._player.steps = max(0, self._player.steps + flee_steps_penalty)
        self.quest_log.appendleft("{} has fled the battle.".format(self._player.name))
        if self._enemy.current_hp < self._enemy.stats[stat_name_to_index('HP')]:
            self.process_exp(10)

    @battle_status(True)
    def enemy_status(self):
        return copy.deepcopy(self._enemy)

    @battle_status(True)
    def battle_stats(self):
        return self._player.combat_stats, self._enemy.combat_stats

