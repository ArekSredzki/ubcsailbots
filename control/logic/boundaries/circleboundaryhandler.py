from control.logic import standardcalc
from control import global_vars as gVars
import time

class CircleBoundaryHandler:

    def __init__(self):
        self.timeSinceBoundaryIntercept = 0 
        self.innerBoundaries = self.getInnerBoundaries(gVars.boundaries)
        self.outerBoundaries = self.getOuterBoundaries(gVars.boundaries)
        gVars.logger.info(str(len(self.innerBoundaries)) + " inner boundaries, " + str(len(self.outerBoundaries)) + " outer boundaries")

    def hitBoundary(self):
        if self.checkBoundaryInterception() and time.time() - self.timeSinceBoundaryIntercept >60:        
            self.timeSinceBoundaryIntercept = time.time()
            gVars.logger.info("Tacking from Boundary")
            return True
        return False
                       
    def checkBoundaryInterception(self,):
        if self.checkInnerBoundaryInterception() or self.checkOuterBoundaryInterception():
            return True
        else:
            return False
    
    def checkInnerBoundaryInterception(self):
        for boundary in self.innerBoundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, gVars.currentData.gps_coord) > boundary.radius):
                return True
        return False
    
    def checkOuterBoundaryInterception(self):
        for boundary in self.outerBoundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, gVars.currentData.gps_coord) <= boundary.radius):
                return True
        return False
    
    def getInnerBoundaries(self, boundaries):
        boundaryList = []
        for boundary in boundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, gVars.currentData.gps_coord) <= boundary.radius):
                boundaryList.append(boundary)
        return boundaryList
                
    def getOuterBoundaries(self, boundaries):
        boundaryList = []
        for boundary in boundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, gVars.currentData.gps_coord) > boundary.radius):
                boundaryList.append(boundary)
        return boundaryList
    
