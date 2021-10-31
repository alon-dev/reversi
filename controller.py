from model import Model

class Controller:
    def __init__(self) -> None:
        self.model = Model()

    def legal_place(self, i,j):
        if self.model.valid((i,j)):
            return True
        return False
    def place(self, i,j):
        if self.model.valid((i,j)):
            self.model.move((i,j))
            return self.model.board
        return None