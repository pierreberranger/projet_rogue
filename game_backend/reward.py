from numpy.random import randint


class Reward:
    
    def __init__(self, symbol="£", hidden=False):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._hidden = hidden

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = randint(0, n_row)
        x_init = randint(0, len(_map[y_init]))
        while _map[y_init][x_init] != ".":
            y_init = randint(0, n_row)
            x_init = randint(0, len(_map[y_init]))

        self._x = x_init
        self._y = y_init

        if not(self._hidden):
            _map[self._y][self._x] = self._symbol
        
    def getPos(self):
        return self._x, self._y

    def getSymbol(self):
        return self._symbol
    
    

        
        