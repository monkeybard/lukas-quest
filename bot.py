from lukas_quest.quest import *

quest = Quest()
for i in range(1000):
    quest.step()
    if quest.quest_log:
        print('At Step {}:'.format(i+1))
        while quest.quest_log:
            print('\t', quest.quest_log.pop())
