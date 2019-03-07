class Player:
    def __init__(self, name):
        self.name = name
        self.is_dead = False
        self.defending = False

        self.hp = 10
        self.attack = 1
        self.defense = 1
        self.magic = 1

        self.baseHp = 10
        self.baseAttack = 1
        self.baseDefense = 1
        self.baseMagic = 1

        self.picture = "220px-Black_square.jpg"

    def take_damage(self, enemy_attack):
        bonus = 0
        if self.defending:
            bonus = 2
            self.defending = False

        if self.is_dead:
            return
        else:
            if self.defense + bonus < enemy_attack:
                self.hp = self.hp - (enemy_attack - self.defense)
            self.die()

    def take_magic_damage(self, enemy_attack):
        bonus = 0
        if self.defending:
            bonus = 2
            self.defending = False

        if self.is_dead:
            return
        else:
            if self.magic + bonus < enemy_attack:
                self.hp = self.hp - (enemy_attack - self.magic)
            self.die()

    def reset_stats(self):
        self.hp = self.baseHp
        self.attack = self.baseAttack
        self.defense = self.baseDefense
        self.magic = self.baseMagic
        self.is_dead = False
        self.defending = False

    def attack_command(self):
        return self.attack

    def defend_command(self):
        return self.defense

    def spell_command(self):
        return self.magic

    def gain_hp(self, recover):
        self.hp = self.hp + recover
        self.die()

    def gain_def(self, boost):
        self.attack = self.attack + boost

    def gain_att(self, boost):
        self.defense = self.defense + boost

    def gain_mag(self, boost):
        self.magic = self.magic + boost

    def die(self):
        if self.hp <= 0:
            self.is_dead = True
        else:
            self.is_dead = False


class Warrior(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.hp = 70
        self.attack = 9
        self.defense = 2
        self.magic = 1

        self.baseHp = 70
        self.baseAttack = 9
        self.baseDefense = 2
        self.baseMagic = 1

        self.picture = "Warrior-ff1-gba.png"


class Mage(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.hp = 30
        self.attack = 2
        self.defense = 3
        self.magic = 7

        self.baseHp = 30
        self.baseAttack = 2
        self.baseDefense = 3
        self.baseMagic = 7

        self.picture = "Blackmage-ff1-gba.png"


class Monk(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.hp = 60
        self.attack = 5
        self.defense = 6
        self.magic = 4

        self.baseHp = 60
        self.baseAttack = 5
        self.baseDefense = 6
        self.baseMagic = 4

        self.picture = "Monk-ff1-wsc.png"


class Thief(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.hp = 30
        self.attack = 7
        self.defense = 3
        self.magic = 2

        self.baseHp = 30
        self.baseAttack = 7
        self.baseDefense = 3
        self.baseMagic = 2

        self.picture = "Thief-ff1-gba.png"
