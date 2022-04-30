from .game_character import GameCharacter

class Monster(GameCharacter):
    def __init__(self, symbol="§"):
        self._symbol = symbol
    
    
    def getSymbol(self):
        return self._symbol
    
    

