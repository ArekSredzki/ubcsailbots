from control.logic import pointtopoint
from control.logic.tacking import chaseracetackengine
from control.logic.roundbuoy import RoundBuoy
from control import global_vars as gVars
from control.logic import standardcalc

class RoundBuoyChaseRace(RoundBuoy):

    def run(self, BuoyLoc):
        gVars.kill_flagRB = 0
        gVars.logger.info("Rounding to " + self.rounding)
        if(self.rounding=="port"):
            point = self.findRightBuoyPoint(BuoyLoc)
        else:
            point = self.findLeftBuoyPoint(BuoyLoc)
        
        gVars.logger.info("Sailing To Rounding Point: " + repr(point))
        if(gVars.kill_flagRB == 0):
            edgeBearing = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, point)
            chaseRaceTackEngine = chaseracetackengine.ChaseRaceTackEngine(self.rounding,edgeBearing)
            self.pointtopoint.withTackEngine(chaseRaceTackEngine).run(point,6)
  
        gVars.logger.info("Finished RoundBuoy")

 