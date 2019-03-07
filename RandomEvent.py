from random import *
from Items import *
from Monster import *


class RandomEvent:
    def __init__(self):
        self.item_choice = Items()
        self.enemy_list = [Bat("Bat"), BigBat("BigBat"), Goblin("Goblin"), BlueGoblin("BlueGoblin"),
                           Dragon("Dragon"), Golem("Golem")]
    # def fight(self):

    def get_item(self):
        return self.item_choice.all_items[randint(0, 7)]

    def get_enemy(self):
        return self.enemy_list[randint(0, len(self.enemy_list)-1)]

    def do_nothing(self):
        return
