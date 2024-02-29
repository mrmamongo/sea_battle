from dataclasses import dataclass
import random

@dataclass
class Ship:
    x_start: int
    y_start: int
    x_end: int
    y_end: int
    type: str
    pos: str


class Ships:
    def __init__(self):
        self.ships_objs = list()
        self.generate()
    
    def generate(self, amount_3d=0, amount_2d=2, amount_1d=3):
        for i in range(amount_3d):
            self.__generate_3d_ship()
        
        for i in range(amount_2d):
            self.ships_objs.append(self.__generate_2d_ship())
        
        for i in range(amount_1d):
            self.ships_objs.append(self.__gererate_1d_ship())

    def get_by_pos(self, x: int, y: int):
        for inx, ship in enumerate(self.ships_objs):
            if ship.x_start <= x <= ship.x_end and ship.y_start <= y <= ship.y_end:
                return (inx, ship)
    
    def __generate_3d_ship(self):
        pass
    
    def __generate_2d_ship(self) -> Ship:
        x_start = random.randint(0, self.size)
        y_start = random.randint(0, self.size)
        pos = random.choice('h', 'v')

        if 'h':
            x_end = x_start + 1
        else:
            y_end = y_start + 1

        return Ship(x_start, y_start, x_end, y_end, '2d', pos)
    
    def __gererate_1d_ship(self) -> Ship:
        x_start = random.randint(0, self.size)
        y_start = random.randint(0, self.size)
        pos = 'h'
        return Ship(x_start, y_start, x_start, y_start, '1d', pos)
