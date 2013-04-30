'''
Created on Apr 14, 2013

@author: joshandrews
'''

import math
from control.logic import standardcalc
from control.logic import pointtopoint
from control import global_vars as gVars
from control.datatype import datatypes
from control import sailing_task

class RoundBuoy(sailing_task.SailingTask):
    #Constants
    TargetAndBuoyAngle = 45
    TargetToBuoyDist = math.sqrt(50)
    MinimumDistance = 10
    
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint
        
    def run(self, BuoyLoc, FinalLoc=None, port=True):
        rightBuoyPoint = self.findRightBuoyPoint(BuoyLoc)
        leftBuoyPoint = self.findLeftBuoyPoint(BuoyLoc)
        
        if(self.distanceBetweenBoatAndBuoyGreaterThanMinDistance(BuoyLoc)):
            self.pointtopoint.run(BuoyLoc,None,self.MinimumDistance,False)
            
        if(port==True):
            self.pointtopoint.run(rightBuoyPoint)
            self.pointtopoint.run(leftBuoyPoint)
        else:
            self.pointtopoint.run(leftBuoyPoint)
            self.pointtopoint.run(rightBuoyPoint)
            
        self.pointtopoint.run(FinalLoc)
        
    def findRightBuoyPoint(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        
        LongitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.cos(self.TargetAndBuoyAngle-angleOfCourse)
        LatitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.sin(self.TargetAndBuoyAngle-angleOfCourse)
        
        rightPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndTarget, LatitudalDistBetweenBuoyAndTarget)
        
        return rightPoint
    
    def findLeftBuoyPont(self, BuoyLoc):
        angleOfCourse = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        
        LongitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.cos(180-(self.TargetAndBuoyAngle+angleOfCourse))
        LatitudalDistBetweenBuoyAndTarget = self.TargetToBuoyDist*math.sin(self.TargetAndBuoyAngle+angleOfCourse)
        
        leftPoint = standardcalc.GPSDistAway(BuoyLoc, LongitudalDistBetweenBuoyAndTarget, LatitudalDistBetweenBuoyAndTarget)
        
        return leftPoint
    
    def distanceBetweenBoatAndBuoyGreaterThanMinDistance(self,BuoyLoc):
        if(standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord,BuoyLoc)>self.MinimumDistance):
            return True
        else:
            return False