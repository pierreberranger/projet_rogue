from .game_character import GameCharacter

class Monster(GameCharacter):
    def __init__(self, _symbol="§"):
        super().__init__(symbol=_symbol)
    
    
    def getSymbol(self):
        return self._symbol
    
    

