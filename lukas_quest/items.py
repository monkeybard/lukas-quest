from lukas_quest.lukas import Lukas

class Preference:
    """Basic decorators that define how preferences affect recovery."""

    @staticmethod
    def modify(lukas, hp_recover, stamina_recover, happiness_change):
        lukas.adjust_hp(hp_recover)
        lukas.adjust_stamina(stamina_recover)
        lukas.adjust_happiness(happiness_change)

    @staticmethod
    def dislike(hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, stamina_recover // 2, -20)
                fun(lukas)
                return "Lukas: I find this hard to palate..."
            return wrapped_f
        return wrap

    @staticmethod
    def neutral(hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, stamina_recover, 0)
                fun(lukas)
                return "Lukas: That was refreshing."
            return wrapped_f
        return wrap

    @staticmethod
    def like(hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, (stamina_recover * 3) // 2, 20)
                fun(lukas)
                return "Lukas: Mmm, a fine meal."
            return wrapped_f
        return wrap

    @staticmethod
    def love(hp_recover, stamina_recover):
        def wrap(fun):
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, stamina_recover * 3, 50)
                fun(lukas)
                return "Lukas: O-oh, now this is a treat!"
            return wrapped_f
        return wrap


class Flavours:
    """Associate flavours with preferences."""
    rough = yucky = Preference.dislike
    plain = refined = Preference.neutral
    rich = bitter = meaty = Preference.like
    sweet = tasty = Preference.love


def pass_fun(lukas):
    pass


# Definitions for foods.
orange = bread_piece = drinking_water = cold_soup = Flavours.plain(10, 10)(pass_fun)
hard_bread = flour = carrot = Flavours.rough(10, 10)(pass_fun)
holey_cheese = Flavours.rich(10, 10)(pass_fun)
soup = Flavours.plain(10, 20)(pass_fun)
garlic = Flavours.refined(10, 30)(pass_fun)
mana_herbs = Flavours.rough(20, 10)(pass_fun)
butter = yogurt = Flavours.rich(20, 10)(pass_fun)
herring = Flavours.plain(20, 10)(pass_fun)
dried_meat = Flavours.meaty(20, 10)(pass_fun)
raw_meat = Flavours.meaty(20, 20)(pass_fun)
honey = Flavours.sweet(30, 20)(pass_fun)
sausage = ham = Flavours.meaty(30, 20)(pass_fun)
dried_shieldfish = Flavours.refined(30, 20)(pass_fun)
sweet_cookie = Flavours.sweet(30, 20)(pass_fun)
blue_cheese = dagon_filet = Flavours.refined(40, 20)(pass_fun)
medicinal_syrup = Flavours.bitter(40, 40)(pass_fun)
exotic_spice = Flavours.refined(10, 50)(pass_fun)
duma_moss = Flavours.yucky(30, 0)(pass_fun)


@Flavours.plain(10, 10)
def leftover_bread(lukas):
    lukas.inventory['bread_piece'] += 1


@Flavours.plain(10, 10)
def bread(lukas):
    lukas.inventory['leftover_bread'] += 1


@Flavours.sweet(0, 40)
def fruit_of_life(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('HP'), 2)


@Flavours.sweet(0, 40)
def soma(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('ATK'), 2)


@Flavours.refined(0, 40)
def nethergranate(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('SKL'), 2)


@Flavours.rich(0, 40)
def pegasus_cheese(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('SPD'), 2)


@Flavours.sweet(0, 40)
def nectar(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('LCK'), 2)


@Flavours.sweet(0, 40)
def ambrosia(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('DEF'), 2)


@Flavours.sweet(0, 40)
def golden_apple(lukas):
    lukas.increase_stat(Lukas.stat_name_to_index('RES'), 2)
