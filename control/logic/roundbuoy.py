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
    TargetToBuoyDist = math.sqrt(50)
    MinimumDistance = 10
    
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint()
        
    def run(self, BuoyLoc, FinalLoc=None, port=True):
        rightBuoyPoint = self.findRightBuoyPoint(BuoyLoc)
        leftBuoyPoint = self.findLeftBuoyPoint(BuoyLoc)
        if FinalLoc is None:
            FinalLoc = datatypes.GPSCoordinate()
            FinalLoc.lat = gVars.currentData.gps_coord.lat
            FinalLoc.long = gVars.currentData.gps_coord.long
            
        if(self.distanceBetweenBoatAndBuoyGreaterThanMinDistance(BuoyLoc)):
            self.pointtopoint.run(BuoyLoc,None,self.MinimumDistance)
            
        if(port==True):
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            self.pointtopoint.run(rightBuoyPoint, 0)
            gVars.logger.info("Final Loc is:" + repr(FinalLoc))
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            self.pointtopoint.run(leftBuoyPoint, None, None, True)
            gVars.logger.info("Final Loc is:" + repr(FinalLoc))
        else:
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            self.pointtopoint.run(leftBuoyPoint, 1)
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            self.pointtopoint.run(rightBuoyPoint, None, None, True)
            
        self.pointtopoint.run(FinalLoc)
        
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
    
    def distanceBetweenBoatAndBuoyGreaterThanMinDistance(self,BuoyLoc):
        if(standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord,BuoyLoc)>self.MinimumDistance):
            return True
        else:
            return False