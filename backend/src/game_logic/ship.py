from dataclasses import dataclass
from exceptions import ShipCreation

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
    def __init__(self, size, tries_to_generate=15, amount_3d=0, amount_2d=2, amount_1d=3):
        self.size = size
        self.tries_to_generate = tries_to_generate
        self.ships_objs = list()
        self.amount_3d = amount_3d
        self.amount_2d = amount_2d
        self.amount_1d = amount_1d
        self.__generate()

    def get_by_pos(self, x: int, y: int):
        for inx, ship in enumerate(self.ships_objs):
            if ship.x_start <= x <= ship.x_end and ship.y_start <= y <= ship.y_end:
                return (inx, ship)
            
    def __generate(self):
        for i in range(self.amount_3d):
            self.ships_objs.append(self.__generate_3d_ship())
        
        for i in range(self.amount_2d):
            self.ships_objs.append(self.__generate_2d_ship())
        
        for i in range(self.amount_1d):
            self.ships_objs.append(self.__gererate_1d_ship())
            
    def __overlap(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        for ship in self.ships_objs:
            if (ship.x_start - 1 <= x1 <= ship.x_end + 1) and (ship.y_start - 1 <= y1 <= ship.y_end + 1) and (ship.x_start - 1 <= x2 <= ship.x_end + 1) and (ship.y_start - 1 <= y2 <= ship.y_end + 1):
                return True
        return False
    
    def __generate_3d_ship(self):
        pass
    
    def __generate_2d_ship(self) -> Ship:
        for i in range(self.tries_to_generate):
            x_start = random.randint(0, self.size-1)
            y_start = random.randint(0, self.size-1)
            x_end = 0
            y_end = 0
            pos = random.choice(['h', 'v'])
            
            if pos == 'h':
                if (y_start <= self.size - 2):
                    y_end = y_start + 1
                else:
                    y_start -= 1
                    y_end = y_start + 1
                x_end = x_start
            else:
                if (x_start <= self.size - 2):
                    x_end = x_start + 1
                else:
                    x_start -= 1
                    x_end = x_start + 1
                y_end = y_start
                
            if not(self.__overlap(x_start, y_start, x_end, y_end)):
                return Ship(x_start, y_start, x_end, y_end, '2d', pos)
        raise ShipCreation("Field is too small to place ships!")
            
    def __gererate_1d_ship(self) -> Ship:
        for i in range(self.tries_to_generate):
            x_start = random.randint(0, self.size-1)
            y_start = random.randint(0, self.size-1)
            pos = 'h'
            if not(self.__overlap(x_start, y_start, x_start, y_start)):
                return Ship(x_start, y_start, x_start, y_start, '1d', pos)
        raise ShipCreation("Field is too small to place ships!")