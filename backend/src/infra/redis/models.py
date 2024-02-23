from dataclasses import dataclass
from enum import Enum

class CellState(str, Enum):
    EMPTY = 'E'
    SHIP = 'S'
    HIT = 'H'
    MISS = 'M'
    SUNK = 'K'


@dataclass
class CellDTO:
    state: CellState
    x: int
    y: int
    ship_size: int
    ship_orientation: str

class BoardDTO():
    def __init__(self, size=5):
        self.size = size
        #Creating clear board size X size
        self.board = [[CellDTO(CellState('E'), x, y) for y in range(size)] for x in range(size)]

@dataclass
class Field:
    cells: BoardDTO


@dataclass
class SessionState:
    pass


@dataclass
class ActiveSession:
    pass
