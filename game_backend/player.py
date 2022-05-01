

from .game_character import GameCharacter
from .monster import Monster
from numpy.random import random, randint

class Player(GameCharacter):
    


    

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy
        win_a_life = map[new_y][new_x] == "£"
        self._life += win_a_life

                    
        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" or map[new_y][new_x] == "£":
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "."
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._html_code}]
            self._x = new_x
            self._y = new_y
        else:
            ret = False
            data = []
        return data, ret, win_a_life

    def nearMonsters(self, monsters):
        near_monsters = 0
        n_damage = 0
        monsters_locations = []
        for monster in monsters:
            x_m, y_m = monster.getPos()
            #if the monster is nearby the player (equivalent to the player is nearby the monster)
            if (x_m, y_m) in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                monsters_locations.append({"i": f"{y_m}", "j":f"{x_m}", "content":monster.getCode()})
                near_monsters += 1
                n_damage += 1 * (random()>monster.getProba())
        return n_damage, near_monsters, monsters_locations, {"i": f"{self._y}", "j":f"{self._x}", "content":"."} #the data is returned in case of death (player should disappear)

    def hitOpponent(self, opponents, map, monsters):
        reachable_opponents = []
        for key, player in opponents.items():
            if player.getPos() in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                reachable_opponents.append((player, key))
        for i, monster in enumerate(monsters):
            if monster.getPos() in [(self._x, self._y+1), (self._x, self._y-1), (self._x+1, self._y), (self._x-1, self._y)] :
                reachable_opponents.append((monster, i))
                
        
        if len(reachable_opponents)!=0 and random()>self._proba_to_hit :
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


