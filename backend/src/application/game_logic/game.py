from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import random

from src.application.game_logic.exceptions import InvalidDoubleDeckerCoordinates


class Orientation(str, Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class Kind(str, Enum):
    SINGLE_DECK = '1d'
    DOUBLE_DECK = '2d'
    TRIPLE_DECK = '3d'


@dataclass
class Ship(ABC):
    # type: Kind

    @abstractmethod
    def collides_with(self, x_start: int, x_end: int, y_start: int, y_end: int) -> bool:
        pass


@dataclass
class SingleDecker(Ship):
    x: int
    y: int
    type: Kind = Kind.SINGLE_DECK

    def collides_with(self, x_start: int, x_end: int, y_start: int, y_end: int) -> bool:
        for x, y in [(x, y) for x in range(x_start, x_end + 1) for y in range(y_start, y_end + 1)]:
            if self.x == x and self.y == y:
                return True
        return False


@dataclass
class DoubleDecker(Ship):
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    type: Kind = Kind.DOUBLE_DECK
    orientation: Orientation = field(init=False, default=Orientation.HORIZONTAL)

    def __post_init__(self):
        if len({self.x_start, self.x_end, self.y_start, self.y_end}) != 2:
            raise InvalidDoubleDeckerCoordinates(self.x_start, self.x_end, self.y_start, self.y_end)
        if not (abs(self.x_end - self.x_start) == 1 or abs(self.y_end - self.y_start) == 1):
            raise InvalidDoubleDeckerCoordinates(self.x_start, self.x_end, self.y_start, self.y_end)

        if self.x_start == self.x_end:
            self.orientation = Orientation.VERTICAL
        else:
            self.orientation = Orientation.HORIZONTAL

    def collides_with(self, x_start: int, x_end: int, y_start: int, y_end: int) -> bool:
        # Check if the ships have overlapping bounding boxes
        if self.x_end < x_start or self.x_start > x_end or self.y_end < y_start or self.y_start > y_end:
            return False
        orientation = Orientation.HORIZONTAL if self.x_start == self.x_end else Orientation.VERTICAL
        # Check if the ships have the same orientation
        if self.orientation == orientation:
            # Check if the ships overlap at any of the four corners
            if self.x_start == x_start and self.y_start == y_start or self.x_start == x_end and self.y_start == y_end or self.x_start == x_start and self.y_end == y_end or self.x_start == x_end and self.y_end == y_start:
                return True
        else:
            # Check if the ships overlap along the longer side of the ship
            if abs(self.x_end - self.x_start) >= abs(
                    self.y_end - self.y_start) and self.x_start <= x_end and self.x_end >= x_start:
                return True
            elif abs(x_end - x_start) >= abs(y_end - y_start) and x_start <= self.x_end and x_end >= self.x_start:
                return True

        # The ships do not collide
        return False


@dataclass
class Board:
    height: int
    width: int
    ships: list[Ship]

    @classmethod
    def generate_new(cls, height: int, width: int, ships_number=None) -> Board:
        if ships_number is None:
            ships_number = [4, 2]

        ships = []
        for i in range(ships_number[0]):
            # Generate random oriented ships in random locations within the board. Check for collisions
            for _ in range(i):
                x_start, y_start = random.randint(0, height - 1), random.randint(0, width - 1)
                x_end, y_end = x_start, y_start
                if random.random() < 0.5:
                    x_end += 1
                else:
                    y_end += 1

                new_ship = SingleDecker(x_start, y_start)

                # Check for collisions
                if not any(
                        ship.collides_with(new_ship.x_start, new_ship.x_end, new_ship.x_start, new_ship.x_end) for ship
                        in ships):
                    ships.append(new_ship)

        for i in range(ships_number[1]):
            ships.append(DoubleDecker(0, 0, 0, 0))

        return cls(height, width, ships)


first = SingleDecker(2, 1)
second = SingleDecker(1, 1)
third = DoubleDecker(2, 1, 1, 1)
print(third.collides_with(first.x, first.x, first.y, first.y))
print(first.collides_with(third.x_start, third.x_end, third.y_start, third.y_end))
print(third.orientation)
