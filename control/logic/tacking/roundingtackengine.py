from control.logic.tacking import tackengine
from control import global_vars as gVars

class RoundingTackEngine(tackengine.TackEngine):

    def __init__(self, rounding):
        self.rounding =rounding
        self.initialTack = rounding                
    
    @property
    def layAngle(self):
        if self.currentTack ==self.rounding:
            return 90
        else:
            return 45

    def onStarboardTack(self,AWA):
        if self.initialTack == "starboard" or  (not self.initialTack and super(RoundingTackEngine, self).onStarboardTack(AWA)):
            self.initialTack = None
            self.currentTack = "starboard"
            return True
        else:
            return False 
            
    def onPortTack(self,AWA):
        if self.initialTack == "port" or (not self.initialTack and super(RoundingTackEngine, self).onPortTack(AWA)):
            self.initialTack = None
            self.currentTack = "port"
            return True
        else:
            return False
            
              