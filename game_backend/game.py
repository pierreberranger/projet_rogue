from .level import Level
from .player import Player

class Game:
    def __init__(self, is_multiplayer=False) -> None:
        self._current_level = 0
        self._is_multiplayer = is_multiplayer
        self._levels = [Level(multiplayer=self._is_multiplayer, level=self._current_level)]
        self._players = dict()
    def getPlayers(self):
        return self._players
    def isMultiplayer(self):
        return self._is_multiplayer
    def removePlayer(self, player_id):
        del self._players[player_id]
    def addPlayer(self, player_id):
        new_player = Player()
        data = new_player.initPos(self._levels[self._current_level].getMap())
        self._players[player_id] = new_player
        print(f"player {player_id} has been added succesfully")
        return data
    def changeLevel(self, player_id):
        increase = self._levels[self._current_level].increaseLevel()
        self._current_level += increase
        if self._current_level > len(self._levels) -1 :
            new_level = Level(multiplayer=self._is_multiplayer, level=self._current_level)
            self._levels.append(new_level)
            ladder_pos = self._levels[self._current_level].getLadderPos(increase)
            self._levels[self._current_level].addPlayer(self._players[player_id], ladder_pos)
        ladder_pos = self._levels[self._current_level].getLadderPos(increase)
        self._players[player_id].setPos(*ladder_pos)
        return self._levels[self._current_level].getMap()
    
    def getMap(self):
        return self._levels[self._current_level].getMap()

    def move(self, dx, dy, player_id):
        return self._levels[self._current_level].move(dx, dy, self._players[player_id])
    
    def is_hit(self, player_id):
        return self._levels[self._current_level].is_hit(self._players[player_id])

    def hitOpponent(self, player_id):
        return self._levels[self._current_level].hitOpponent(self._players[player_id], self._players)       