from numpy.random import randint, random

class GameCharacter:
    def __init__(self, symbol="@", html_code="""<img src="static\player.png" alt=""></img>""", initial_life=5, proba_to_hit=0.2, hidden=False, in_multiplayer_game=False):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._life = initial_life
        self._proba_to_hit = proba_to_hit
        if in_multiplayer_game:
            self._proba_to_hit = 0.5
        self._hidden = hidden
        self._html_code = html_code
    
    def getPos(self):
        return self._x, self._y
    
    def getCode(self):
        return self._html_code

    def getLife(self):
        return self._life

    def getSymbol(self):
        return self._symbol
    
    def getProba(self):
        return self._proba_to_hit

    def changeLife(self, new_life):
        self._life += new_life
        return self._life <= 0
        print(f"changed life to {self._life}")
    
    def setPos(self, x, y):
        self._x = x
        self._y = y
        
    def remove(self, map, symbol):
        map[self._y][self._x] = symbol

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
    
    def hitOpponent(self, opponents, map, monsters):
        reachable_opponents = []
        for key, player in opponents.items():
            if player.getPos() in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                reachable_opponents.append((player, key))
        for i, monster in enumerate(monsters):
            if monster.getPos() in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                reachable_opponents.append((monster, i))
                
        
        if len(reachable_opponents)!=0 and random()<self._proba_to_hit :
            reached_opponent, opponent_id = reachable_opponents[randint(0,len(reachable_opponents))]
            is_dead = reached_opponent.changeLife(-1)
            x, y = reached_opponent.getPos()
            if isinstance(opponent_id, int) and is_dead:
                del monsters[opponent_id]
                print("wow un monstre tué")
                map[y][x] = "."
            elif is_dead:
                del opponents[opponent_id]
                map[y][x] = "."
            return True, opponent_id, is_dead, {"i": f"{y}", "j":f"{x}", "content":"."}
        return False, None, False, None



    