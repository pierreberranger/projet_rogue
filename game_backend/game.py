from .map_generator import Generator
from .player import Player
from time import sleep


class Game:
    def __init__(self, width=96, height=32, time_between_hits=1):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._generator.gen_rewards()
        self._map = self._generator.tiles_level
        self._monsters = self._generator.gen_monsters()
        self._time_between_hits = time_between_hits

        self._player = Player()
        self._player.initPos( self._map )

    def getMap(self):
        return self._map
    
    def getLife(self):
        return self._player._life

    def move(self, dx, dy):
        #self.near_monsters(self._map)
        return self._player.move(dx, dy, self._map)
    
    def hits(self):
        near_monsters, monsters_locations = self._player.nearMonsters(self._monsters)
        is_dead = self._player.changeLife(-near_monsters)
        return near_monsters != 0, near_monsters, is_dead, monsters_locations

            
    
    