from functools import partial
from lukas_quest.config import *
from lukas_quest.unit import stat_name_to_index


def clean_name(item_name):
    return item_name.replace('_', ' ').title()


class Preference:
    """Basic decorators that define how preferences affect recovery."""

    @staticmethod
    def modify(player, hp_recover, stamina_recover, happiness_change):
        player.adjust_hp(hp_recover)
        player.adjust_stamina(stamina_recover)
        player.adjust_happiness(happiness_change)

    @staticmethod
    def preference(stamina_mult, happiness, reaction, hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(player, log):
                Preference.modify(player, hp_recover, int(stamina_recover * stamina_mult), happiness)
                log.appendleft(reaction)
                fun(player, log)
            setattr(wrapped_f, 'isfood', None)
            return wrapped_f
        return wrap

    dislike = partial(preference.__get__(object), 0.5, -20, dislike_line)
    neutral = partial(preference.__get__(object), 1, 0, neutral_line)
    like = partial(preference.__get__(object), 1.5, 20, like_line)
    love = partial(preference.__get__(object), 3, 50, love_line)


class Flavours:
    """Associate flavours with preferences."""
    rough = yucky = Preference.dislike
    plain = refined = Preference.neutral
    rich = bitter = meaty = Preference.like
    sweet = tasty = Preference.love


def _pass_fun(player, log):
    pass


# Definitions for foods.
orange = bread_piece = drinking_water = cold_soup = Flavours.plain(10, 10)(_pass_fun)
hard_bread = flour = carrot = Flavours.rough(10, 10)(_pass_fun)
holey_cheese = Flavours.rich(10, 10)(_pass_fun)
soup = Flavours.plain(10, 20)(_pass_fun)
garlic = Flavours.refined(10, 30)(_pass_fun)
mana_herbs = Flavours.rough(20, 10)(_pass_fun)
butter = yogurt = Flavours.rich(20, 10)(_pass_fun)
herring = Flavours.plain(20, 10)(_pass_fun)
dried_meat = Flavours.meaty(20, 10)(_pass_fun)
raw_meat = Flavours.meaty(20, 20)(_pass_fun)
honey = Flavours.sweet(30, 20)(_pass_fun)
sausage = ham = Flavours.meaty(30, 20)(_pass_fun)
dried_shieldfish = Flavours.refined(30, 20)(_pass_fun)
sweet_cookie = Flavours.sweet(30, 20)(_pass_fun)
blue_cheese = dagon_filet = Flavours.refined(40, 20)(_pass_fun)
medicinal_syrup = Flavours.bitter(40, 40)(_pass_fun)
exotic_spice = Flavours.refined(10, 50)(_pass_fun)
duma_moss = Flavours.yucky(30, 0)(_pass_fun)


@Flavours.plain(10, 10)
def leftover_bread(player, log):
    player.inventory['bread_piece'] += 1
    log.appendleft("Bread Piece added to inventory.")


@Flavours.plain(10, 10)
def bread(player, log):
    player.inventory['leftover_bread'] += 1
    log.appendleft("Leftover Bread added to inventory.")


@Flavours.sweet(0, 40)
def fruit_of_life(player, log):
    increase = player.increase_stat(stat_name_to_index('HP'), 2)
    if increase:
        log.appendleft("HP increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def soma(player, log):
    increase = player.increase_stat(stat_name_to_index('ATK'), 2)
    if increase:
        log.appendleft("ATK increased by {}.".format(increase))


@Flavours.refined(0, 40)
def nethergranate(player, log):
    increase = player.increase_stat(stat_name_to_index('SKL'), 2)
    if increase:
        log.appendleft("SKL increased by {}.".format(increase))


@Flavours.rich(0, 40)
def pegasus_cheese(player, log):
    increase = player.increase_stat(stat_name_to_index('SPD'), 2)
    if increase:
        log.appendleft("SPD increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def nectar(player, log):
    increase = player.increase_stat(stat_name_to_index('LCK'), 2)
    if increase:
        log.appendleft("LCK increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def ambrosia(player, log):
    increase = player.increase_stat(stat_name_to_index('DEF'), 2)
    if increase:
        log.appendleft("DEF increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def golden_apple(player, log):
    increased = player.levelup()
    if any(increased):
        log.appendleft("Levelled up!")
        log.appendleft(player.stats)


foods = [food for food in globals() if hasattr(globals()[food], 'isfood')]
