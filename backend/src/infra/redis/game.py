from models import CellDTO, BoardDTO

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