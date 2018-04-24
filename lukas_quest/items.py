def dislike(lukas):
    lukas.adjust_stamina(20)
    lukas.adjust_happiness(-20)
    return lukas.adjust_hp(5), "I find this hard to palate..."


def neutral(lukas):
    lukas.adjust_stamina(30)
    return lukas.adjust_hp(10), "That was refreshing."


def like(lukas):
    lukas.adjust_stamina(50)
    lukas.adjust_happiness(20)
    return lukas.adjust_hp(15), "Mmm, a fine meal."


def love(lukas):
    lukas.adjust_stamina(100)
    lukas.adjust_happiness(50)
    return lukas.adjust_hp(20), "O-oh, now this is a treat!"


def flour(lukas):
    return dislike(lukas)


def ham(lukas):
    return neutral(lukas)


def blue_cheese(lukas):
    return like(lukas)


def sweet_cookie(lukas):
    return love(lukas)
