from lukas_quest.quest import *

quest = Quest()
i = 1
while True:
    quest.step()
    status = quest.status
    if status.stamina == 0:
        if list(quest.get_inventory().elements()):
            quest.use(list(quest.get_inventory().elements())[0])
        else:
            print(status.level, status.happiness, status.stats)
            break
    if quest.quest_log:
        print('At Step {}:'.format(i))
        while quest.quest_log:
            print('\t', quest.quest_log.pop())
    i += 1
