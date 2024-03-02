from src.infra.redis.models import CellDTO, BoardDTO, CellState
from ship import Ship, Ships, Kind, Position

from dataclasses import dataclass
from exceptions import GameTry

import random

class Game:
    def __init__(self, size=10):
        self.size = size
        self.board = BoardDTO(size)
        self.ships = Ships(size, amount_2d=0, amount_1d=1)
        self.game_state = 'Started'
        self.__place_ships()

    def __place_ships(self):
        for ship in self.ships.ships_objs:
            for i in range(ship.x_start, ship.x_end+1):
                for j in range(ship.y_start, ship.y_end+1):
                    self.board.board[i][j] = CellDTO(CellState('ship'))
        
    def __repr__(self) -> str:
        output = ''
        for i in range(self.size):
            for j in range(self.size):
                output += str(self.board.board[i][j].state) + ' '
            output += '\n'
        return output

    def shoot(self, row, col):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            raise ValueError('Coordinate is beyond the board')
        
        if len(self.ships.ships_objs) == 0:
            raise GameTry("All ships are dead!")

        cell = self.board.board[row][col]

        if cell.state == 'ship':
            inx, ship = self.ships.get_by_pos(row, col)
            if ship.type == '1d':
                self.hit(ship, inx)
            elif ship.type == '2d':
                if ship.pos == 'horizontal':
                    max_col = min(col+1, self.size - 1)
                    min_col = max(col-1, 0)
                    if self.board.board[row][max_col].state == 'hit' or self.board.board[row][min_col].state == 'hit':
                        self.hit(ship, inx)
                    else:
                        cell.state = CellState('hit')
                else:
                    max_row = min(row+1, self.size - 1) 
                    min_row = max(0, row-1)
                    if self.board.board[max_row][col].state == 'hit' or self.board.board[min_row][col].state == 'hit':
                        self.hit(ship, inx)
                    else:
                        cell.state = CellState('hit')
                    
        elif cell.state == 'cross':
            cell.state = CellState('miss')
        else:
            raise ValueError('This cell was already hit')

    def hit(self, ship, inx):
        self.make_empty(ship)
        self.make_sunk(ship)
        self.ships.ships_objs.pop(inx)
        if len(self.ships.ships_objs) == 0:
            self.game_state = 'Over'

    def make_empty(self, ship: Ship):
        x_start = max(0, ship.x_start-1)
        x_end = min(self.size, ship.x_end+2)
        y_start = max(0, ship.y_start-1)
        y_end = min(self.size, ship.y_end+2)
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                self.board.board[i][j].state = CellState('empty')
    
    def make_sunk(self, ship: Ship):
        if ship.pos == 'horizontal':
            max_col = min(ship.y_end+1, self.size)
            for j in range(ship.y_start, max_col):
                self.board.board[ship.x_start][j].state = CellState('sunk')
        else:
            max_row = min(ship.x_end+1, self.size)
            for i in range(ship.x_start, max_row):
                self.board.board[i][ship.y_start].state = CellState('sunk')
