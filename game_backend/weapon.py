from .reward import Reward
from random import choices

class Weapon(Reward):
    
    def __init__(self, symbol="%", hidden=True):
        super().__init__(symbol, hidden)
        self._accuracy_increase = choices([0.1, 0.2, 0.4, 0.8], weights=[100, 50, 10, 2], k=1)[0]

    def getAccuracyIncrease(self):
        return self._accuracy_increase