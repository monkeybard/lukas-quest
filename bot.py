from lukas_quest.quest import *

new_quest = Quest()
status = new_quest.status
print(status.current_hp, status.steps)
new_quest._lukas.adjust_hp(-10)
new_quest.step()
status = new_quest.status
print(status.current_hp, status.steps)
new_quest.save()