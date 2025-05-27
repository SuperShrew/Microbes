
class Cell:
    def __init__(self, type, parent_id):
        self.icons = {
            "mover": "m",
            "mouth": "M",
            "producer": "P",
            "killer": "K",
            "armour": "A",
            "blank": " "
        }
        self.type = type
        self.icon = self.icons[type]
        self.parent_id = parent_id
