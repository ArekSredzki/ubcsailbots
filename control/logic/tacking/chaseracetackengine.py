from control.logic.tacking.roundingtackengine import RoundingTackEngine
from control import global_vars as gVars
from control.logic import standardcalc

class ChaseRaceTackEngine(RoundingTackEngine):
    
    BEARING_DELTA_THRESHOLD = 2
    def __init__(self, rounding,edgeBearing):
          self.edgeBearing = edgeBearing
          super(ChaseRaceTackEngine,self).__init__(rounding)
      
    def readyToTack(self, AWA, HOG, bearing):
        return super(ChaseRaceTackEngine,self).readyToTack(AWA, HOG, bearing) or self.hitBoxBoundary(bearing)
    
    def hitBoxBoundary(self,bearing):
        if self.currentTack != self.rounding:
            bearingDelta = standardcalc.calculateAngleDelta(bearing, self.edgeBearing)
            if abs(bearingDelta)<self.BEARING_DELTA_THRESHOLD:
                gVars.logger.info("Tacked from box boundary")
                return True
            else:
                return False
        else:
            return False