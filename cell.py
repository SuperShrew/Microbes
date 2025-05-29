from colours import Clr

class Cell:
    def __init__(self, type, parent_id):
        self.c = Clr()
        self.icons = {
            "mover": self.c.CYAN + "m",
            "mouth": self.c.YELLOW + "M",
            "producer": self.c.GREEN + "P",
            "killer": self.c.RED + "K",
            "armour": self.c.MAGENTA + "A",
            "food": self.c.BLUE + "F",
            "blank": " "
        }
        self.type = type
        self.icon = self.icons[type]
        self.parent_id = parent_id
