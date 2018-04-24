from functools import wraps


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
            @wraps(fun)
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, stamina_recover // 2, -20)
                fun(lukas)
                return "Lukas: I find this hard to palate..."
            return wrapped_f
        return wrap

    @staticmethod
    def neutral(hp_recover, stamina_recover):
        def wrap(fun):
            @wraps(fun)
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, stamina_recover, 0)
                fun(lukas)
                return "Lukas: That was refreshing."
            return wrapped_f
        return wrap

    @staticmethod
    def like(hp_recover, stamina_recover):
        def wrap(fun):
            @wraps(fun)
            def wrapped_f(lukas):
                Preference.modify(lukas, hp_recover, (stamina_recover * 3) // 2, 20)
                fun(lukas)
                return "Lukas: Mmm, a fine meal."
            return wrapped_f
        return wrap

    @staticmethod
    def love(hp_recover, stamina_recover):
        def wrap(fun):
            @wraps(fun)
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


@Flavours.plain(10, 10)
def leftover_bread(lukas):
    lukas.inventory['bread_piece'] += 1


@Flavours.plain(10, 10)
def bread(lukas):
    lukas.inventory['leftover_bread'] += 1
