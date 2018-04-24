from lukas_quest.quest import *

quest = Quest()
for i in range(1000):
    quest.step()
    while quest.quest_log:
        print('{:3}:'.format(i+1), quest.quest_log.pop())
