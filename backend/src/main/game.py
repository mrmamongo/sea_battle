from enum import Enum

class CellState(str, Enum):
    EMPTY = 'E'
    SHIP = 'S'
    HIT = 'H'
    MISS = 'M'
    SUNK = 'K'

class CellDTO:
    def __init__(self, state, x, y, ship_size=0, ship_orientation=None):
        self.state = state
        self.x = x
        self.y = y
        self.ship_size = ship_size
        self.ship_orientation = ship_orientation

    def to_cell_state(self):
        if self.state == 'E':
            return CellState.EMPTY
        elif self.state == 'S':
            return CellState.SHIP
        elif self.state == 'H':
            return CellState.HIT
        elif self.state == 'M':
            return CellState.MISS
        elif self.state == 'K':
            return CellState.SUNK

class BoardDTO:
    def __init__(self, size=5):
        self.size = size
        #Creating clear board size X size
        self.board = [[CellDTO('E', x, y) for y in range(size)] for x in range(size)]

class BoardShooterDTO:
    def __init__(self, size=5):
        self.size = size

    def shoot(self, board, row, col):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            raise ValueError('Coordinate is beyond the board')
        

        cell = board.board[row][col]
        if cell.state == 'S':
            cell.state = 'H'
            for ship in board.ships:
                if ship[0] == cell.ship_size and ship[1] == row and ship[2] == col and ship[3] == 'horizontal':
                    board.ships.remove(ship)
                    for i in range(cell.ship_size):
                        if ship[3] == 'horizontal':
                            board.board[row][col + i].state = 'K'
                        else:
                            board.board[row + i][col].state = 'K'
                    return CellDTO('K', row, col)
                elif ship[0] == cell.ship_size and (ship[1] == row and ship[2] == col or ship[1] == row and ship[2] == col + 1 or ship[1] == row + 1 and ship[2] == col or ship[1] == row - 1 and ship[2] == col):
                    cell.state = 'H'
                    for i in range(cell.ship_size):
                        if ship[3] == 'horizontal':
                            board.board[row][col + i].state = 'K'
                        else:
                            board.board[row + i][col].state = 'K'
                    return CellDTO('K', row, col)
        else:
            cell.state = 'M'
            return CellDTO('M', row, col)