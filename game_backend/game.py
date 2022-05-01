from .map_generator import Generator
from .player import Player


class Game:
    def __init__(self, width=96, height=32, time_between_hits=1, hidden_monsters=True):
        self._generator = Generator(width=width, height=height, hidden_monsters=hidden_monsters)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._generator.gen_rewards()
        self._map = self._generator.tiles_level
        self._monsters = self._generator.gen_monsters()
        self._time_between_hits = time_between_hits
        self._players = dict()

    def removePlayer(self, player_id):
        del self._players[player_id]

    def getMap(self):
        return self._map

    def getPlayers(self):
        return self._players

    def addPlayer(self, player_id):
        new_player = Player()
        data = new_player.initPos(self._map)
        self._players[player_id] = new_player
        print(f"player {player_id} has been added succesfully")
        return data
    
    def move(self, dx, dy, player_id):
        return self._players[player_id].move(dx, dy, self._map)
    
    def is_hit(self, player_id):
        n_damage, near_monsters, monsters_locations, data = self._players[player_id].nearMonsters(self._monsters)
        is_dead = self._players[player_id].changeLife(-n_damage)
        if is_dead:
            x, y = self._players[player_id].getPos()
            self._map[y][x] = "."
        return near_monsters != 0, n_damage!=0, n_damage, is_dead, monsters_locations, data

    def hitOpponent(self, player_id):
        return self._players[player_id].hitOpponent(self._players, self._map, self._monsters)            
    
    