from .game_character import GameCharacter

class Monster(GameCharacter):
    def __init__(self, _symbol="§", html_code="""<img src="static\monster.png" alt=""></img>""", initial_life=5, proba_to_hit=0.5, hidden=False):
        super().__init__(symbol=_symbol, html_code=html_code, initial_life=initial_life, proba_to_hit=proba_to_hit, hidden=hidden)
    
    

