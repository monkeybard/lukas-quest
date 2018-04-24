from lukas_quest.quest import *

quest = Quest()
while True:
    if quest.in_battle:
        e_status = quest.enemy_status()
        print('\t', e_status.level, e_status.current_hp, e_status.stats)
        quest.resolve_phase()
    else:
        quest.step()
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

