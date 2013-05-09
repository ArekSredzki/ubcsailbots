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
    MinimumDistance = 10
    
    def __init__(self, port=True):
        self.port = port
        self.pointtopoint = pointtopoint.PointToPoint()
        
    def run(self, BuoyLoc, FinalLoc=None):
        gVars.kill_flagRB = 0
        
        rightBuoyPoint = self.findRightBuoyPoint(BuoyLoc)
        leftBuoyPoint = self.findLeftBuoyPoint(BuoyLoc)
        rightInitialPoint = self.findRightInitialPoint(BuoyLoc)
        leftInitialPoint = self.findLeftInitialPoint(BuoyLoc)
        
        if FinalLoc is None:
            FinalLoc = datatypes.GPSCoordinate()
            FinalLoc.lat = gVars.currentData.gps_coord.lat
            FinalLoc.long = gVars.currentData.gps_coord.long
                        
        if(self.distanceBetweenBoatAndBuoyGreaterThanMinDistance(BuoyLoc)):
            if(self.port):
                gVars.logger.info("Sailing To Right Initial Point: " + repr(rightInitialPoint))
                if(gVars.kill_flagRB == 0):
                    self.pointtopoint.run(rightInitialPoint, None, 8)
            else:
                gVars.logger.info("Sailing To Left Initial Point: " + repr(leftInitialPoint))
                if(gVars.kill_flagRB == 0):
                    self.pointtopoint.run(leftInitialPoint, None, 8)
            
        if(self.port==True):
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(rightBuoyPoint, 0,6)
            #gVars.logger.info("Final Loc is:" + repr(FinalLoc))
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(leftBuoyPoint, None, 6, True)
            #gVars.logger.info("Final Loc is:" + repr(FinalLoc))
        else:
            gVars.logger.info("Sailing To Left Buoy Point: " + repr(leftBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(leftBuoyPoint, 1,6)
            gVars.logger.info("Sailing To Right Buoy Point: " + repr(rightBuoyPoint))
            if(gVars.kill_flagRB == 0):
                self.pointtopoint.run(rightBuoyPoint, None, 6, True)
        
        if(gVars.kill_flagRB == 0):
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
    
    def findRightInitialPoint(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        angleFromEast = 90-angleOfCourse
        
        LongitudalDistBetweenBuoyAndInitialSailPoint = self.InitialSailToBuoyDist*math.cos(math.radians(angleFromEast-self.InitialSailAndBuoyAngle))
        LatitudalDistBetweenBuoyAndInitialSailPoint = self.InitialSailToBuoyDist*math.sin(math.radians(angleFromEast-self.InitialSailAndBuoyAngle))
        
        rightInitialPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndInitialSailPoint, LatitudalDistBetweenBuoyAndInitialSailPoint)
        
        return rightInitialPoint
    
    def findLeftInitialPoint(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        angleFromEast = 90-angleOfCourse
        
        LongitudalDistBetweenBuoyAndInitialSailPoint = self.InitialSailToBuoyDist*math.cos(math.radians(angleFromEast+self.InitialSailAndBuoyAngle))
        LatitudalDistBetweenBuoyAndInitialSailPoint = self.InitialSailToBuoyDist*math.sin(math.radians(angleFromEast+self.InitialSailAndBuoyAngle))
        
        leftInitialPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndInitialSailPoint, LatitudalDistBetweenBuoyAndInitialSailPoint)
        
        return leftInitialPoint
    
    def distanceBetweenBoatAndBuoyGreaterThanMinDistance(self,BuoyLoc):
        if(standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord,BuoyLoc)>self.MinimumDistance):
            return True
        else:
            return False