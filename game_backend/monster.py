from .game_character import GameCharacter

class Monster(GameCharacter):
    def __init__(self, _symbol="§", initial_life=5, proba_to_hit=0.5, hidden=False):
        super().__init__(symbol=_symbol, initial_life=initial_life, proba_to_hit=proba_to_hit, hidden=hidden)
    
    

