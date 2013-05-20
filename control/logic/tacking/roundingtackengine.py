from control.logic.tacking import tackengine
from control import global_vars as gVars

class RoundingTackEngine(tackengine.TackEngine):
    
    def __init__(self, rounding):
        self.rounding =rounding
        self.initialTack = rounding        
        
    def readyToTack(self, AWA, HOG, bearing): 
        self.setLayAngle(AWA)
        if self.hitLayLine(HOG, bearing, self.layAngle) and  self.beatEstablished(AWA):
            gVars.logger.info("Hit  "+str(self.layAngle)+" degree lay line")
            return True
        else:
            return False
    
    def setLayAngle(self, AWA):
        if self.onStarboardTack(AWA):
            self.setLayAngleStarboard()
        else:
            self.setLayAnglePort()
                
    def setLayAngleStarboard(self):
        if self.rounding == "starboard":
            self.layAngle = 90
        else: #ie starboard tack
            self.layAngle = 45

    def setLayAnglePort(self):
        if self.rounding == "starboard":
            self.layAngle = 45
        else: #ie starboard tack
            self.layAngle = 90        
                       
            
    def onStarboardTack(self,AWA):
        if self.initialTack == "starboard":
            self.initialTack = None
            return True
        else:
            return  tackengine.TackEngine.onStarboardTack(self,AWA)
            
    def onPortTack(self,AWA):
        if self.initialTack == "port":
            self.initialTack = None
            return True
        else:
            return tackengine.TackEngine.onPortTack(self,AWA)
            
              