from Player import *


class Monster(Player):
    def __init__(self, name):
        Player.__init__(self, name)


class Bat(Monster):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 10
        self.attack = 10
        self.defense = 1
        self.magic = 1

        self.picture = "WildBat.png"


class BigBat(Bat):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 20
        self.attack = 10
        self.defense = 2
        self.magic = 2

        self.picture = "WildBat.png"


class Goblin(Monster):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 30
        self.attack = 10
        self.defense = 3
        self.magic = 1

        self.picture = "Goblin_ATB.png"

class BlueGoblin(Goblin):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 60
        self.attack = 10
        self.defense = 3
        self.magic = 6

        self.picture = "Goblin_ATB.png"

class Dragon(Monster):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 300
        self.attack = 10
        self.defense = 1
        self.magic = 2

        self.picture = "Ffiigreendragon_psp.png"

class Golem(Monster):
    def __init__(self, name):
        Monster.__init__(self, name)
        self.hp = 100
        self.attack = 10
        self.defense = 1
        self.magic = 1

        self.picture = "FF4PSP_Steel_Golem.png"