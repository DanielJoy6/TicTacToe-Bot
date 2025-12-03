from abc import ABC, abstractmethod
class Player(ABC):
    
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def makeMove(self, board, gametype):
        pass
    
    def reset(self):
        pass
    def __repr__(self):
        return self.name
