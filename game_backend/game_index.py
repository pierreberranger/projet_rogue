from collections import UserDict



GameIndex = UserDict
def generateId(game_index):
    if game_index !={}:
        return str(int(max(game_index.keys()))+1)
    return "0"
