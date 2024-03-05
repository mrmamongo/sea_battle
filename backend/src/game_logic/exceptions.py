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