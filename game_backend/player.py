

from .game_character import GameCharacter
from .monster import Monster
from numpy.random import random, randint

class Player(GameCharacter):
    


    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = n_row//2
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init

        _map[self._y][self._x] = self._symbol
        return {"i": f"{self._y}", "j":f"{self._x}", "content":self._symbol}

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy
        win_a_life = map[new_y][new_x] == "£"
        self._life += win_a_life

                    
        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" or map[new_y][new_x] == "£":
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        else:
            ret = False
            data = []
        return data, ret, win_a_life

    def nearMonsters(self, monsters):
        near_monsters = 0
        monsters_locations = []
        for monster in monsters:
            x_m, y_m =monster.getPos()
            if (x_m, y_m) in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                monsters_locations.append({"i": f"{y_m}", "j":f"{x_m}", "content":monster.getSymbol()})
                near_monsters += 1
        return near_monsters, monsters_locations

    def changeLife(self, new_life):
        self._life += new_life
        return self._life <= 0

    def hitOpponent(self, opponents, map):
        reachable_opponents = []
        for key, player in opponents.items():
            if player.getPos() in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                reachable_opponents.append(key)
        if len(reachable_opponents)!=0 and random()>self._proba_to_hit :
            reached_opponent = reachable_opponents[randint(0,len(reachable_opponents))]
            is_dead= opponents[reached_opponent].changeLife(-1)
            x, y = opponents[reached_opponent].getPos()
            map[y][x] = "."
            return True, reached_opponent, is_dead, {"i": f"{y}", "j":f"{x}", "content":"."}
        return False, None, False, None


