from control.logic.tacking import tackengine
from control.logic import standardcalc
from control import global_vars as gVars

class P2PTackEngine(tackengine.TackEngine):
    
    def __init__(self):
        self.layAngle = 75

    def readyToTack(self, AWA, HOG, bearing):        
        if self.hitLayLine(HOG, bearing, self.layAngle) and  self.beatEstablished(AWA):
            gVars.logger.info("Hit  "+str(self.layAngle)+" degree lay line")
            return True
        else:
            return False