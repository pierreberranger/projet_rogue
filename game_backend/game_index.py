from ast import If
from collections import UserDict
from xml.dom import UserDataHandler
from .game import Game


GameIndex = UserDict
def generateId(game_index):
    if game_index !={}:
        return str(int(max(game_index.keys()))+1)
    return "0"
