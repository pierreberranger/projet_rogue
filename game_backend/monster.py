from .game_character import GameCharacter

monster_level = [(1, 0), (1, 0.3), (2, 0.3), (2, 0.4), (2, 0.5), (3, 0.5), (3, 0.6), 
                (4, 0.5), (4, 0.6), (5, 0.6), (5, 0.7), (6, 0.6), (6, 0.7), (7, 0.6), 
                (7, 0.7), (7, 0.8), (8, 0.7), (8, 0.8), (8, 0.9), (9, 0.8), (9, 0.9)]

class Monster(GameCharacter):
    def __init__(self, _symbol="§", html_code="""<img src="static\monster.png" alt=""></img>""", level=0, hidden=False):
        if level > len(monster_level) - 1:
            life, proba_to_hit =monster_level[-1]
        else:
            life, proba_to_hit =monster_level[level]
        
        super().__init__(symbol=_symbol, html_code=html_code, initial_life=life, proba_to_hit=proba_to_hit, hidden=hidden)
    
    

