from dataclasses import dataclass
from enum import Enum

class CellState(str, Enum):
    CROSS = 'cross'
    EMPTY = 'empty'
    SHIP = 'ship'
    HIT = 'hit'
    MISS = 'miss'
    SUNK = 'sunk'


@dataclass
class CellDTO:
    state: CellState

class BoardDTO():
    def __init__(self, size=5):
        self.size = size
        #Creating clear board size X size
        self.board = [[CellDTO(CellState('cross')) for y in range(size)] for x in range(size)]

@dataclass
class Field:
    cells: BoardDTO


@dataclass
class SessionState:
    pass


@dataclass
class ActiveSession:
    pass
