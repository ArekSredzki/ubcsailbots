'''
Created on Apr 14, 2013

@author: joshandrews
'''

from os import path
from control.parser import parsing
from control.logic import standardcalc
from control.datatype import datatypes
from control import static_vars as sVars
from control import global_vars as gVars
from control import sailing_task
import math
import time


class PointToPoint(sailing_task.SailingTask):
    #constants
    COMPASS_METHOD = 0
    COG_METHOD = 1
    AWA_METHOD = 2
    TACKING_ANGLE = 30
    ANGLE_CHANGE_THRESHOLD = 5

    def __init__(self):
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
        self.initialTack = None
        self.innerBoundaries = self.getInnerBoundaries(gVars.boundaries)
        self.outerBoundaries = self.getOuterBoundaries(gVars.boundaries)
        gVars.logger.info("New Point to Point object")
        gVars.logger.info(str(len(self.innerBoundaries)) + " inner boundaries, " + str(len(self.outerBoundaries)) + " outer boundaries")
          
    def initialize(self):
        self.oldTackSailing = 0
        self.tackSailing = 0
        self.oldAWA = 0
        self.oldColumn = 0
        self.oldAngleBetweenCoords = 0
        self.tackDirection = 0
        self.printedStraight = 0
        self.layAngle = 75
        self.timeSinceBoundaryIntercept = 0
                
    # --- Point to Point ---
    # Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own, TWA = 0 for sailing using only AWA and 1 for attempting to find TWA.
    # Output: Nothing
    def run(self, Dest, initTack = None, acceptDist=None, roundingLayOffset =0):
        self.initialize()
        gVars.logger.info("Started point to pointAWA toward "+repr(Dest))
        self.Dest = Dest
        self.roundingLayOffset = roundingLayOffset
        self.updateData()
        gVars.kill_flagPTP = 0
        self.initialTack = initTack
        if acceptDist == None:
            self.ACCEPTANCE_DISTANCE = sVars.ACCEPTANCE_DISTANCE_DEFAULT
        else:
            self.ACCEPTANCE_DISTANCE = acceptDist
        while(not self.arrivedAtPoint()) and gVars.kill_flagPTP == 0:
            self.updateData()
   
            if(standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord)):
                self.printedStraight = 0
                
                if(self.starboardTackWanted(self.initialTack)):
                    self.enterBeatLoop(False)
                    
                elif(self.portTackWanted(self.initialTack)):
                    self.enterBeatLoop(True) 
                    
            else:                    
                if(self.printedStraight == 0):
                    gVars.logger.info("Sailing straight to point")
                    self.printedStraight = 1
                self.tackSailing = 3
                if(self.isThereChangeToAWAorWeatherOrModeOrAngle()):
                    self.adjustSheetsAndSteerByCompass()                    
            time.sleep(.1)

        if(gVars.kill_flagPTP == 1):
            gVars.logger.info("PointToPoint is killed")
        else:
            gVars.logger.info("Finished Point to Point")

        return

    def enterBeatLoop(self, port):
        if port:
            self.tackSailing = 2
            gVars.logger.info("On port tack")
            tackAngleMultiplier = -1
        else:
            self.tackSailing = 1
            gVars.logger.info("On starboard tack")
            tackAngleMultiplier = 1
        
        self.initialTack = None
        
        while(gVars.kill_flagPTP ==0):
            self.updateData()
            if self.arrivedAtPoint() or self.canLayMarkWithoutTack():
                break              
            if self.readyToTack() or self.breakFromBoundaryInterception():
                self.setTackDirection()
                gVars.arduino.tack(gVars.currentColumn,self.tackDirection)
                break          
            if self.isThereChangeToAWAorWeatherOrMode():
                self.adjustSheetsAndSteerByApparentWind(tackAngleMultiplier)
            time.sleep(.1)
                     
    def adjustSheetsAndSteerByCompass(self):
        gVars.arduino.adjust_sheets(self.sheetList[abs(int(self.AWA))][gVars.currentColumn])
        gVars.arduino.steer(self.COMPASS_METHOD,self.angleBetweenCoords)  
            
    def adjustSheetsAndSteerByApparentWind(self, tackAngleMultiplier):
        gVars.arduino.adjust_sheets(self.sheetList[abs(int(self.AWA))][gVars.currentColumn])
        gVars.arduino.steer(self.AWA_METHOD,tackAngleMultiplier*self.TACKING_ANGLE)
        
    def updateData(self):
        self.GPSCoord = gVars.currentData.gps_coord
        self.distanceToWaypoint = standardcalc.distBetweenTwoCoords(self.GPSCoord, self.Dest)
        self.AWA = gVars.currentData.awa
        self.cog = gVars.currentData.cog
        self.hog = gVars.currentData.hog
        self.sog = gVars.currentData.sog * 100
        self.angleBetweenCoords = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
        standardcalc.getWeatherSetting(self.AWA,self.sog)

    def arrivedAtPoint(self):
        return self.distanceToWaypoint < self.ACCEPTANCE_DISTANCE  
       
    def killPointToPoint(self):
        gVars.kill_flagPTP = 1
        
    def starboardTackWanted(self,initialTack):
        if( (self.AWA>=0 and initialTack is None) or initialTack == 1 ):
            return 1
        else:
            return 0
            
    def portTackWanted(self,initialTack):
        if( (self.AWA<0 and initialTack is None) or initialTack == 0 ):
            return 1
        else:
            return 0
    
    def readyToTack(self):
        if self.tackSailing==1: #ie port tack
            self.layAngle = 75+self.roundingLayOffset
        elif self.tackSailing==2: #ie starboard tack
            self.layAngle = 75-self.roundingLayOffset
        
        beatEstablished =(abs(abs(self.AWA)- self.TACKING_ANGLE)<10)

        if(abs(standardcalc.calculateAngleDelta(self.hog,standardcalc.angleBetweenTwoCoords(self.GPSCoord, self.Dest))) < self.layAngle):
            return False
        elif beatEstablished:
            gVars.logger.info("Hit  "+str(self.layAngle)+" degree lay line")
            return True
        else:
            return False
        
    def isThereChangeToAWAorWeatherOrModeOrAngle(self):
        if(self.AWA != self.oldAWA or self.oldColumn != gVars.currentColumn or self.oldTackSailing != self.tackSailing or abs(self.oldAngleBetweenCoords-self.angleBetweenCoords)>self.ANGLE_CHANGE_THRESHOLD):
            self.updateOldData()
            return 1
        else:
            self.updateOldData()
            return 0

    def isThereChangeToAWAorWeatherOrMode(self):
        if(self.AWA != self.oldAWA or self.oldColumn != gVars.currentColumn or self.oldTackSailing != self.tackSailing):
            self.updateOldData()
            return 1
        else:
            self.updateOldData()
            return 0
             
    def updateOldData(self):
        self.oldAWA = self.AWA
        self.oldColumn = gVars.currentColumn
        self.oldTackSailing = self.tackSailing
        self.oldAngleBetweenCoords = self.angleBetweenCoords
    
    def breakFromBoundaryInterception(self):
        if self.checkBoundaryInterception() and time.time() - self.timeSinceBoundaryIntercept >60:        
            self.timeSinceBoundaryIntercept = time.time()
            gVars.logger.info("Tacking from Boundary")
            return True
        return False
                       
    def checkBoundaryInterception(self):
        if self.checkInnerBoundaryInterception() or self.checkOuterBoundaryInterception():
            return True
        else:
            return False
    
    def checkInnerBoundaryInterception(self):
        for boundary in self.innerBoundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, self.GPSCoord) > boundary.radius):
                return True
        return False
    
    def checkOuterBoundaryInterception(self):
        for boundary in self.outerBoundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, self.GPSCoord) <= boundary.radius):
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
    
    # Sets 1, or 0 for Arduino Call to Tack
    def setTackDirection(self):
        if(self.AWA > 0):
            self.tackDirection = 1
        else:
            self.tackDirection = 0
            
    def canLayMarkWithoutTack(self):
        if standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord):
            return False
        else:
            windDirection = standardcalc.boundTo180(self.AWA + self.hog)
            bearing = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
            return not standardcalc.isAngleBetween(bearing,windDirection,self.hog)      
                
