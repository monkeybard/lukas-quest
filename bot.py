from lukas_quest import items
from lukas_quest.quest import *

new_quest = Quest()
new_quest._lukas.adjust_hp(-10)
new_quest._lukas.adjust_happiness(250)
new_quest._lukas.adjust_stamina(-250)
status = new_quest.status
print(status.happiness, status.stamina, status.current_hp, status.inventory)
foods = [food for food in dir(items)
         if callable(getattr(items, food)) and not food.startswith('__') and not food[0].isupper()]
print(foods)
for food in foods:
    print("Eating", food.replace('_', ' ').title())
    new_quest.give(food)
    print(new_quest.use(food))
    status = new_quest.status
    print(status.happiness, status.stamina, status.current_hp, status.inventory)
