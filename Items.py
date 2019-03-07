class Items:
    def __init__(self):
        self.healing_items = ["HP+10", "HP+30"]
        self.attack_items = ["Attack+1", "Attack+3"]
        self.defense_items = ["Defense+1", "Defense+3"]
        self.magic_items = ["Magic+1", "Magic+3"]
        self.all_items = self.attack_items + self.healing_items + self.defense_items + self.magic_items