

from .game_character import GameCharacter
from .monster import Monster
from numpy.random import random, randint
from .weapon import Weapon

class Player(GameCharacter):

    def move(self, dx, dy, map, on_object, weapons):
        new_x = self._x + dx
        new_y = self._y + dy
        win_a_life = map[new_y][new_x] == "£"
        self._life += win_a_life
        on_ladder = map[new_y][new_x] == "^" or map[new_y][new_x] == "_"
        new_on_object = on_object
        new_weapon = map[new_y][new_x] == "%"
        if new_weapon:
            for weapon in weapons:
                x_weapon, y_weapon = weapon.getPos()
                if (x_weapon, y_weapon) == (new_x, new_y):
                    weapon_found = weapon
            weapons.remove(weapon_found)
            if self._proba_to_hit + weapon_found.getAccuracyIncrease() <= 1:
                self._proba_to_hit += weapon_found.getAccuracyIncrease()  
            else:
                self._proba_to_hit = 1
                self._life +=1
                print("new weapon : life increase")
            print(f"weapon found: accuracy increase: {weapon_found.getAccuracyIncrease()}, proba to hit your opponents: {self._proba_to_hit}")
        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" or map[new_y][new_x] == "£" or map[new_y][new_x] == "^" or map[new_y][new_x] == "_"  or map[new_y][new_x] == "%":
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
            ret = False
            data = []
        return data, ret, win_a_life, on_ladder, new_on_object, new_weapon

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
                n_damage += 1 * (random()<monster.getProba())
        return n_damage, near_monsters, monsters_locations, {"i": f"{self._y}", "j":f"{self._x}", "content":"."} #the data is returned in case of death (player should disappear)

    