from src.infra.redis.models import CellDTO, BoardDTO
from ship import Ship, Ships

from dataclasses import dataclass
import random

class Game:
    def __init__(self, size=10):
        self.size = size
        self.board = BoardDTO(size=size)
        self.ships = Ships(self.board)

    def shoot(self, row, col):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            raise ValueError('Coordinate is beyond the board')

        cell = self.board.board[row][col]

        if cell.state == 'ship':
            inx, ship = self.ships.get_by_pos(row, col)
            if ship.type == '1d':
                self.hit(ship, inx)
            elif ship.type == '2d':
                if ship.pos == 'h':
                    if self.board.board[row+1, col] == 'hit':
                        self.hit(ship, inx)
                else:
                    if self.board.board[row, col+1] == 'hit':
                        self.hit(ship, inx)
            else:
                pass
        elif cell.state == 'cross':
            cell.state = 'miss'
        else:
            raise ValueError('This cell was already hit')

    def hit(self, ship, inx):
        self.make_empty(ship)
        self.make_sunk(ship)
        self.ships.ships_objs.pop(inx)
        if len(self.ships.ships_objs) == 0:
            return "Game over!"

    def make_empty(self, ship: Ship):
        x_start = max(0, ship.x_start-1)
        x_end = min(self.size, ship.x_end+1) + 1
        y_start = min(0, ship.y_start-1)
        y_end = min(self.size, ship.y_end+1) + 1
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                self.board.board[i][ship.y_start].state = 'empty'
    
    def make_sunk(self, ship: Ship):
        if ship.type == 'h':
            for i in range(ship.x_start, ship.x_end+1):
                self.board.board[i][ship.y_start].state = 'sunk'
        else:
            for j in range(ship.y_start, ship.y_end+1):
                self.board.board[ship.x_start][j].state = 'sunk'
