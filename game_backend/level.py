from .map_generator import Generator
from .player import Player
from game_backend import player


class Level:
    def __init__(self, width=96, height=32, time_between_hits=1, hidden_monsters=True, multiplayer=False, level=0):
        self._generator = Generator(width=width, height=height, hidden_monsters=hidden_monsters, ground_floor=(level==0), multiplayer=multiplayer)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._generator.gen_rewards()
        self._ladders = self._generator.add_ladder()
        self._generator.gen_weapons()
        self._map = self._generator.tiles_level
        self._monsters = self._generator.gen_monsters()
        self._time_between_hits = time_between_hits
        self._players = dict()
        self._multiplayer = multiplayer
        self._difficulty = level
        if level==0:
            self._on_object = "."
        else:
            self._on_object = "_"
    
    def isMultiplayer(self):
        return self._multiplayer
    def removePlayer(self, player):
        x, y = player.getPos()
        self._map[y][x] = "."

    def getMap(self):
        return self._map

    def getPlayers(self):
        return self._players
    
    def getOnObject(self):
        return self._on_object

    def addPlayer(self, player, pos):
        data = player.initPos(self._map, pos)
    
    def move(self, dx, dy, player):
        data, ret, win_a_life, on_ladder, self._on_object = player.move(dx, dy, self._map, self._on_object)
        return data, ret, win_a_life, on_ladder
    def is_hit(self, player):
        n_damage, near_monsters, monsters_locations, data = player.nearMonsters(self._monsters)
        is_dead = player.changeLife(-n_damage)
        if is_dead:
            x, y = player.getPos()
            self._map[y][x] = "."
        return near_monsters != 0, n_damage!=0, n_damage, is_dead, monsters_locations, data

    def hitOpponent(self, player, players):
        return player.hitOpponent(players, self._map, self._monsters)            
    
    def increaseLevel(self):
        increase = 0
        if self._on_object == "_":
            increase = -1
        elif self._on_object == "^":
            increase = 1
        print(increase)
        return increase
    def getLadderPos(self, increase):
        if increase == 1:
            return self._ladders[-1].getPos()
        else:
            return tuple(self._ladders[0].getPos())
    def resetLadders(self):
        for ladder in self._ladders :
            x, y = ladder.getPos()
            self._map[y][x] = ladder.getSymbol()

        
        