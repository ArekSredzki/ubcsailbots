'''
Created on Apr 14, 2013

@author: joshandrews
'''

import math
from control.logic import standardcalc
from control.logic import pointtopoint
from control.datatype import datatypes
from control import global_vars as gVars
from control import sailing_task

class RoundBuoy(sailing_task.SailingTask):
    #Constants
    TargetAndBuoyAngle = 45
    TargetToBuoyDist = 12
    
    def __init__(self):
        self.rounding = gVars.instructions.rounding
        self.pointtopoint = pointtopoint.PointToPoint()
        
    def run(self, BuoyLoc, fullRound = True):
        gVars.kill_flagRB = 0
        gVars.logger.info("Rounding to " + self.rounding)
        if(self.rounding=="port"):
            point1 = self.findRightBuoyPoint(BuoyLoc)
            point2 = self.findLeftBuoyPoint(BuoyLoc)
            initialTack = 0
            roundingLayOffset =-20
        else:
            point1 = self.findLeftBuoyPoint(BuoyLoc)
            point2 = self.findRightBuoyPoint(BuoyLoc)
            initialTack = 1
            roundingLayOffset =20
        
        gVars.logger.info("Sailing To 1st Rounding Point: " + repr(point1))
        if(gVars.kill_flagRB == 0):
            self.pointtopoint.run(point1, initialTack,6, roundingLayOffset)
            
        if fullRound:
            gVars.logger.info("Sailing To 2nd Rounding Point: " + repr(point2))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(point2, None, 6)
       
        gVars.logger.info("Finished RoundBuoy")

    def findRightBuoyPoint(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        angleFromEast = 90-angleOfCourse
        
        LongitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.cos(math.radians(angleFromEast-self.TargetAndBuoyAngle))
        LatitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.sin(math.radians(angleFromEast-self.TargetAndBuoyAngle))
        
        rightPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndTarget, LatitudalDistBetweenBuoyAndTarget)
        
        return rightPoint
    
    def findLeftBuoyPoint(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        angleFromEast = 90-angleOfCourse
        
        LongitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.cos(math.radians(angleFromEast+self.TargetAndBuoyAngle))
        LatitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.sin(math.radians(angleFromEast+self.TargetAndBuoyAngle))
        
        leftPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndTarget, LatitudalDistBetweenBuoyAndTarget)
        
        return leftPoint
 