from numpy.random import randint

class GameCharacter:
    def __init__(self, symbol="@", initial_life=5):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._life = initial_life

    def initPos(self, _map, hidden=False):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = randint(0, n_row)
        x_init = randint(0, len(_map[y_init]))
        while _map[y_init][x_init] != ".":
            y_init = randint(0, n_row)
            x_init = randint(0, len(_map[y_init]))

        self._x = x_init
        self._y = y_init

        if not(hidden):
            _map[self._y][self._x] = self._symbol
    
    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        else:
            ret = False
            data = []
        return data, ret
    def getLife(self):
        return self._life