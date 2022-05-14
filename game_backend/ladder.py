from .reward import Reward

class Ladder(Reward):
    
    def __init__(self, symbol="^", hidden=False):
        super().__init__(symbol, hidden=hidden)
    
    def getType(self):
        return self._type
    
