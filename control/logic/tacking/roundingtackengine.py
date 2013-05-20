from control.logic.tacking import tackengine
from control import global_vars as gVars

class RoundingTackEngine(tackengine.TackEngine):
    
    def __init__(self, rounding):
        self.rounding =rounding
        self.initialTack = rounding                

    def getLayAngle(self):
        if self.currentTack =="starboard":
            return self.setLayAngleStarboard()
        elif self.currentTack =="port":
            return self.setLayAnglePort()
                
    def setLayAngleStarboard(self):
        if self.rounding == "starboard":
            return 90
        else: #ie starboard tack
            return 45

    def setLayAnglePort(self):
        if self.rounding == "starboard":
            return 45
        else: #ie starboard tack
            return 90        
                       
            
    def onStarboardTack(self,AWA):
        if self.initialTack == "starboard" or  tackengine.TackEngine.onStarboardTack(self,AWA):
            self.initialTack = None
            self.currentTack = "starboard"
            return True
        else:
            return False 
            
    def onPortTack(self,AWA):
        if self.initialTack == "port" or tackengine.TackEngine.onPortTack(self,AWA):
            self.initialTack = None
            self.currentTack = "port"
            return True
        else:
            return False
            
              