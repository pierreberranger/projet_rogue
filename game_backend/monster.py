from .game_character import GameCharacter
import numpy as np

monster_level = [(1, 0, 2), (1, 0.3, 2), (2, 0.3), (2, 0.4), (2, 0.5), (3, 0.5), (3, 0.6),
                 (4, 0.5), (4, 0.6), (5, 0.6), (5,
                                                0.7), (6, 0.6), (6, 0.7), (7, 0.6),
                 (7, 0.7), (7, 0.8), (8, 0.7), (8, 0.8), (8, 0.9), (9, 0.8), (9, 0.9)]


class Monster(GameCharacter):

    def __init__(self,  _symbol="§", html_code="""<img src="static\monster3.png" alt=""></img>""", level=0, hidden=False):
        if level > len(monster_level) - 1:
            life, proba_to_hit, move_frequency = monster_level[-1]
        else:
            life, proba_to_hit, move_frequency = monster_level[level]
        self.move_frequency = move_frequency
        self.compteur_move = 0
        self.symbol = _symbol
        super().__init__(symbol=_symbol, html_code=html_code,
                         initial_life=life, proba_to_hit=proba_to_hit, hidden=hidden)

    def move(self, map):
        self.compteur_move += 1

        if self.compteur_move % self.move_frequency == 0:
            delta = np.random.randint(3, size=2)
            new_x = self._x + (delta[0]-1)
            new_y = self._y + (delta[1]-1)

            if map[new_y][new_x] == "." or map[new_y][new_x] == "x":
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "."
                data = [{"i": f"{self._y}", "j": f"{self._x}", "content": "."}, {
                    "i": f"{new_y}", "j": f"{new_x}", "content": self.symbol}]
                self._x = new_x
                self._y = new_y
                return data, ret
            elif map[new_y][new_x] == "G":
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "x"
                data = [{"i": f"{self._y}", "j": f"{self._x}", "content": "."}, {
                    "i": f"{new_y}", "j": f"{new_x}", "content": self.symbol}]
                self._x = new_x
                self._y = new_y
                return data, ret
            elif map[new_y][new_x] == "&":
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "x"
                data = [{"i": f"{self._y}", "j": f"{self._x}", "content": "."}, {
                    "i": f"{new_y}", "j": f"{new_x}", "content": self.symbol}]
                self._x = new_x
                self._y = new_y
                return data, ret
            elif map[new_y][new_x] == "#":
                ret = False
                data = []
                return data, ret
            else:
                ret = False
                data = []
                return data, ret
        else:
            ret = False
            data = []
            return data, ret
