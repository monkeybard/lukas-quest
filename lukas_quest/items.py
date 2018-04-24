from functools import partial
from lukas_quest.lukas import Unit


def clean_name(item_name):
    return item_name.replace('_', ' ').title()

class Preference:
    """Basic decorators that define how preferences affect recovery."""

    @staticmethod
    def modify(lukas, hp_recover, stamina_recover, happiness_change):
        lukas.adjust_hp(hp_recover)
        lukas.adjust_stamina(stamina_recover)
        lukas.adjust_happiness(happiness_change)

    @staticmethod
    def preference(stamina_mult, happiness, reaction, hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(lukas, log):
                Preference.modify(lukas, hp_recover, int(stamina_recover * stamina_mult), happiness)
                log.appendleft(reaction)
                fun(lukas, log)
            setattr(wrapped_f, 'isfood', None)
            return wrapped_f
        return wrap

    dislike = staticmethod(partial(preference.__get__(object), 0.5, -20, "Lukas: I find this hard to palate..."))
    neutral = staticmethod(partial(preference.__get__(object), 1, 0, "Lukas: That was refreshing."))
    like = staticmethod(partial(preference.__get__(object), 1.5, 20, "Lukas: Mmm, a fine meal."))
    love = staticmethod(partial(preference.__get__(object), 3, 50, "Lukas: O-oh, now this is a treat!"))


class Flavours:
    """Associate flavours with preferences."""
    rough = yucky = Preference.dislike
    plain = refined = Preference.neutral
    rich = bitter = meaty = Preference.like
    sweet = tasty = Preference.love


def _pass_fun(lukas, log):
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
def leftover_bread(lukas, log):
    lukas.inventory['bread_piece'] += 1
    log.appendleft("Bread Piece added to inventory.")


@Flavours.plain(10, 10)
def bread(lukas, log):
    lukas.inventory['leftover_bread'] += 1
    log.appendleft("Leftover Bread added to inventory.")


@Flavours.sweet(0, 40)
def fruit_of_life(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('HP'), 2)
    if increase:
        log.appendleft("Lukas' HP increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def soma(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('ATK'), 2)
    if increase:
        log.appendleft("Lukas' ATK increased by {}.".format(increase))


@Flavours.refined(0, 40)
def nethergranate(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('SKL'), 2)
    if increase:
        log.appendleft("Lukas' SKL increased by {}.".format(increase))


@Flavours.rich(0, 40)
def pegasus_cheese(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('SPD'), 2)
    if increase:
        log.appendleft("Lukas' SPD increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def nectar(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('LCK'), 2)
    if increase:
        log.appendleft("Lukas' LCK increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def ambrosia(lukas, log):
    increase = lukas.increase_stat(Unit.stat_name_to_index('DEF'), 2)
    if increase:
        log.appendleft("Lukas' DEF increased by {}.".format(increase))


@Flavours.sweet(0, 40)
def golden_apple(lukas, log):
    increased = lukas.levelup()
    if any(increased):
        log.appendleft("Levelled up!")
        log.appendleft(lukas.stats)


foods = [food for food in globals() if hasattr(globals()[food], 'isfood')]
