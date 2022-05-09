from .reward import Reward

class Weapon(Reward):
    def __init__(self, symbol="%", hidden=True):
        super().__init__(symbol, hidden)