'''
Created on Apr 14, 2013

@author: joshandrews
'''

from os import path
from control.parser import parsing
from control.logic import standardcalc
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
    ACCEPTANCE_DISTANCE=3

    def __init__(self):
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
        self.initialTack = None
        gVars.logger.info("New Point to Point object")
          
    def initialize(self):
        self.oldTackSailing = 0
        self.tackSailing = 0
        self.oldAWA = 0
        self.oldColumn = 0
        self.oldAngleBetweenCoords = 0
        self.tackDirection = 0
        self.printedStraight = 0
    
    # --- Point to Point ---
    # Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own, TWA = 0 for sailing using only AWA and 1 for attempting to find TWA.
    # Output: Nothing
    def run(self, Dest, initTack = None, noTack = False):
        self.initialize()
        gVars.logger.info("Started point to pointAWA toward "+repr(Dest))
        self.Dest = Dest
        self.updateData()
        gVars.kill_flagPTP = 0
        self.initialTack = initTack

        while(not self.arrivedAtPoint()) and gVars.kill_flagPTP == 0:
            time.sleep(.1)
            self.updateData()
   
            if(standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord) and noTack == False):
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
                self.handleBoundaries()



        if(gVars.kill_flagPTP == 1):
            gVars.logger.info("PointToPoint is killed")
        else:
            gVars.logger.info("Finished Point to Point")

        return

    def enterBeatLoop(self, port):
        tackAngleMultiplier = -1
        if port:
            self.tackSailing = 2
            gVars.logger.info("On port tack")
        else:
            self.tackSailing = 1
            gVars.logger.info("On starboard tack")
            tackAngleMultiplier = 1
        
        self.initialTack = None
        gVars.tacked_flag = 0

        while(self.doWeStillWantToTack()):
            time.sleep(.1)
            if(self.arrivedAtPoint()):
                gVars.tacked_flag=1
                break
            else:
                gVars.tacked_flag = 0
            self.updateData()
                                       
            if(self.isThereChangeToAWAorWeatherOrMode() ):
                self.adjustSheetsAndSteerByApparentWind(tackAngleMultiplier)
   
            self.setTackDirection()
            
            self.handleBoundaries()
            if(gVars.tacked_flag):
                break
         
        if(gVars.tacked_flag == 0):                                                                
            gVars.arduino.tack(gVars.currentColumn,self.tackDirection)
            gVars.logger.info("Tacked from 80 degrees")

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
    
    def doWeStillWantToTack(self):
        if(abs(standardcalc.calculateAngleDelta(self.hog,standardcalc.angleBetweenTwoCoords(self.GPSCoord, self.Dest))) < 80 and gVars.kill_flagPTP ==0):
            return 1
        else:
            return 0
        
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

    def handleBoundaries(self):
        boundary = self.checkBoundaryInterception()
        if boundary is not None:
            self.sailFromBoundary(boundary)
        return
    
    def checkBoundaryInterception(self):
        for boundary in gVars.boundaries:
            if(standardcalc.distBetweenTwoCoords(boundary.coordinate, self.GPSCoord) <= boundary.radius):
                return boundary
        return None
    
    def sailFromBoundary(self, boundary):
        sinAngle = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord,boundary.coordinate)
        sinAngle = abs(sinAngle)
        
        dist_to_boundary = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boundary.coordinate)
        x_dist = dist_to_boundary * math.sin(math.radians(sinAngle))
        
        if(gVars.currentData.gps_coord.long < boundary.coordinate.long):
            x_dist=-x_dist
            
        gVars.logger.info("Tacked from boundary")
        gVars.arduino.tack(gVars.currentColumn,self.tackDirection)
        gVars.tacked_flag = 1
        
        return
    # Sets 1, or 0 for Arduino Call to Tack
    def setTackDirection(self):
        if(self.AWA > 0):
            self.tackDirection = 0
        else:
            self.tackDirection = 1