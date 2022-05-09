

from .game_character import GameCharacter
from .monster import Monster
from numpy.random import random, randint

class Player(GameCharacter):
    


    

    def move(self, dx, dy, map, on_object):
        new_x = self._x + dx
        new_y = self._y + dy
        win_a_life = map[new_y][new_x] == "£"
        self._life += win_a_life
        on_ladder = map[new_y][new_x] == "^" or map[new_y][new_x] == "_"
        print(on_ladder)
        new_on_object = on_object            
        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" or map[new_y][new_x] == "£" or map[new_y][new_x] == "^" or map[new_y][new_x] == "_" :
            ret = True
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._html_code}]
            map[self._y][self._x] = "."
            if on_object == "^" or on_object == "_":
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content": """<img src="static\\ladder.png" sizes=""></img>"""}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._html_code}]
                map[self._y][self._x] = on_object
            new_on_object = map[new_y][new_x]
            map[new_y][new_x] = self._symbol
            self._x = new_x
            self._y = new_y
        else:
            print(map[new_y][new_x])
            ret = False
            data = []
        print(data, ret, win_a_life, on_ladder, new_on_object)
        return data, ret, win_a_life, on_ladder, new_on_object

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


