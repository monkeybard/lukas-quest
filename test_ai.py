from lukas_quest.quest import *

quest = Quest()

for i in range(200):
    quest.step()
    while quest.in_battle:
        e_status = quest.enemy_status()
        quest.resolve_phase()
    status = quest.status
    if status.stamina == 0 and not quest.in_battle:
        if list(quest.get_inventory().elements()):
            quest.use(list(quest.get_inventory().elements())[0])
        else:
            print('Final Level: ', status.level, ', Final Happiness: ', status.happiness,
                  ', Final Stats: ', status.stats, sep='')
            break

    if quest.quest_log:
        status = quest.status
        print('At Step {}:'.format(status.steps))
        while quest.quest_log:
            print('\t', quest.quest_log.pop())

print('Current Level: ', status.level, ', Current Happiness: ', status.happiness,
      ', Current Stats: ', status.stats, sep='')
quest.save()
