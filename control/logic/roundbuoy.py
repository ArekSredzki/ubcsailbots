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
    InitialSailAndBuoyAngle = 135
    TargetToBuoyDist = 12
    InitialSailToBuoyDist = 20
    
    def __init__(self):
        self.rounding = gVars.instructions.rounding
        self.pointtopoint = pointtopoint.PointToPoint()
        
    def run(self, BuoyLoc):
        gVars.kill_flagRB = 0
        
        rightBuoyPoint = self.findRightBuoyPoint(BuoyLoc)
        leftBuoyPoint = self.findLeftBuoyPoint(BuoyLoc)
 
        if(self.rounding=="port"):
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(rightBuoyPoint, 0,6, roundingLayOffset =-20)
            #gVars.logger.info("Final Loc is:" + repr(FinalLoc))
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(leftBuoyPoint, None, 6)
            #gVars.logger.info("Final Loc is:" + repr(FinalLoc))
        elif (self.rounding=="starboard"):
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(leftBuoyPoint, 1,6, roundingLayOffset =20)
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(rightBuoyPoint, None, 6)
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
 