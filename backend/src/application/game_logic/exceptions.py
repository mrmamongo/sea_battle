class ShipCreation(Exception):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return self.message

class GameTry(Exception):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return self.message

class InvalidDoubleDeckerCoordinates(Exception):
    def __init__(self, x_start: int, x_end: int, y_start: int, y_end: int):
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

    def __str__(self) -> str:
        return f'Invalid double decker coordinates: ({self.x_start}, {self.x_end}), ({self.y_start}, {self.y_end})'