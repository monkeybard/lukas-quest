import numpy
from collections import Counter
from lukas_quest.classes import *
from lukas_quest.weapons import *

# Basic configuration file to ease reskinning Lukas Quest to <Somebody> Quest.
# More in-depth mechanics changes will require editing other files.
#### Player information
filepath = './lukas_quest/lukas.save'
player_name = 'Lukas'
default_feclass = Soldier()
default_level = 2
default_exp = 0
default_stats = numpy.array([22, 10, 4, 4, 2, 5, 2])
default_stat_caps = numpy.array([52, 40, 40, 38, 40, 42, 40])
default_growth_rates = numpy.array([50, 30, 40, 25, 30, 45, 20])
#### Lines
out_of_stamina = "{}: I'm afraid... I can walk no further...".format(player_name)
## Said when eating food. Flavour preferences should be defined in items.py.
dislike_line = "{}: I find this hard to palate...".format(player_name)
neutral_line = "{}: That was refreshing.".format(player_name)
like_line = "{}: Mmm, a fine meal.".format(player_name)
love_line = "{}: O-oh, now this is a treat!".format(player_name)
#### Quest starting status
default_stamina = 500
default_happiness = 0
default_inventory = Counter()
default_steps = 0
#### Quest settings
## An event will be triggered every time the number of steps is divisible by anything in event_intervals.
event_intervals = [20, 30]
## Probability distribution for the likelihood of [find_item, give_exp, trigger_battle]
event_dist = [0.6, 0.1, 0.3]
## Possible foods that can be dropped by an event. Default is all.
from lukas_quest.items import foods
item_drops = foods
## Probability distribution for the likelihood of each item drop (from an event) is.
# Need to be an array of floats from 0.0 to 1.0 the same length as item_drops, all adding up to 1.0.
# Probabilities correspond 1:1 with the possible drops.
# By default every food is can be dropped by an event.
# Common (70%) = [orange, bread_piece, ..., raw_meat, leftover_bread, bread]
# Uncommon (25%) = [honey, sausage, ..., duma_moss]
# Rare (5%) = [fruit_of_life, soma, ..., golden_apple]
item_dist = [0.7/18]*16 + [0.25/10]*10 + [0.7/18]*2 + [0.05/7]*7
## Possible amounts of exp that can be gained in an event.
exp_drops = [10, 15, 25, 50, 100]
## Probability distribution for the likelihood of that amount of exp being gained. Same as food_dist mechanically.
exp_dist = [0.5, 0.25, 0.125, 0.1, 0.025]
## Every enemy_level_increase_interval steps the maximum possible level of the enemies will increase.
enemy_level_increase_interval = 50
## Enemies will spawn at any level in the range [max_level - enemy_level_variance, max_level]
enemy_level_variance = 3
## Enemy map
# Format: After how many Steps will these enemies appear : [(Types of Enemies)], [Probability Distribution]
# Enemy Format: Class, [[Possible Weapons], [Probability Distribution]], [[Possible Drops], [Probability Distribution]]
enemy_map = {
    0: ([
        (Brigand(), [[IronAxe()], [1]], [['drinking_water', 'hard_bread', 'sweet_cookie'], [0.3, 0.5, 0.2]])
        ],
        [1]),
    100: ([
          (Brigand(), [[IronAxe(), DevilAxe()], [0.9, 0.1]],
           [['leftover_bread', 'drinking_water', 'sweet_cookie'], [0.3, 0.4, 0.3]])
          ],
          [1])
}
## Boss map
# A boss will always appear at that step number, weapon is set and a name, level and base stats can be specified.
# Drops are same as above.
boss_map = {
    100: (Brigand(), 'Garth', DevilAxe(), 5, None, [['dried_meat', 'sweet_cookie', 'fruit_of_life'], [0.7, 0.29, 0.01]])
}
## Penalties
death_happiness_penalty = -50
death_steps_penalty = -50
flee_happiness_penalty = -5
flee_steps_penalty = -30
