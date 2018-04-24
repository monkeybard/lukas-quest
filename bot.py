from lukas_quest.quest import *

quest = Quest()
for i in range(500):
    quest.step()
    while quest.quest_log:
        print(quest.quest_log.pop())
