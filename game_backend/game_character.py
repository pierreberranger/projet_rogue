from numpy.random import randint

class GameCharacter:
    def __init__(self, symbol="@", html_code="""<img src="static\player.png" alt=""></img>""", initial_life=5, proba_to_hit=0.1, hidden=False):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._life = initial_life
        self._proba_to_hit = proba_to_hit
        self._hidden = hidden
        self._html_code = html_code
    
    def getPos(self):
        return self._x, self._y
    
    def getCode(self):
        return self._html_code

    def initPos(self, _map, pos=None):
        n_row = len(_map)
        #n_col = len(_map[0])
        if pos == None :
            y_init = randint(0, n_row)
            x_init = randint(0, len(_map[y_init]))
            while _map[y_init][x_init] != ".":
                y_init = randint(0, n_row)
                x_init = randint(0, len(_map[y_init]))
        else:
            x_init, y_init = pos
        self._x = x_init
        self._y = y_init

        if not(self._hidden):
            _map[self._y][self._x] = self._symbol
            return {"i": f"{self._y}", "j":f"{self._x}", "content":self._html_code}
        return None
    
    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            ret = True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "."
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._html_code}]
            self._x = new_x
            self._y = new_y
        else:
            ret = False
            data = []
        return data, ret
    def getLife(self):
        return self._life
    
    def changeLife(self, new_life):
        self._life += new_life
        return self._life <= 0
    
    def getSymbol(self):
        return self._symbol
    
    def getProba(self):
        return self._proba_to_hit
    
    def remove(self, map, symbol):
        map[self._y][self._x] = symbol
    def setPos(self, x, y):
        self._x = x
        self._y = y
        
    