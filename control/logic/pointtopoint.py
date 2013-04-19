'''
Created on Apr 14, 2013

@author: joshandrews
'''

from os import path
from control.parser import parsing
from control.logic import standardcalc
from control import StaticVars as sVars
from control import GlobalVars as gVars
from control import sailingtask
import math
import time


class PointToPoint(sailingtask.SailingTask):
    #constants
    COMPASS_METHOD = 0
    COG_METHOD = 1
    AWA_METHOD = 2
    TACKING_ANGLE = 34
    ANGLE_CHANGE_THRESHOLD = 5

    def __init__(self):
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
        self.tackSailing = 0
        self.newTackSailing = 0
        self.AWA = 0
        self.oldColumn = 0
        self.oldAngleBetweenCoords = 0
        self.tackDirection = 0
        self.printedStraight = 0
        gVars.kill_flagPTP = 0
        gVars.logger.info("New Point to Point object")

        
    # --- Point to Point ---
    # Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own, TWA = 0 for sailing using only AWA and 1 for attempting to find TWA.
    # Output: Nothing
    def run(self, Dest, initialTack = None, ACCEPTANCE_DISTANCE = sVars.ACCEPTANCE_DISTANCE_DEFAULT):
        time.sleep(1.0)
        gVars.logger.info("Started point to pointAWA")
        self.Dest = Dest
        self.updateData()
        
        while(self.distanceToWaypoint < ACCEPTANCE_DISTANCE) and gVars.kill_flagPTP == 0:
            time.sleep(.1)
            self.updateData()

            #This if statement determines the sailing method we are going to use based on apparent wind angle
            standardcalc.getWeatherSetting(self.newAWA,self.sog)
                #print ("Hit else statement")
                #print ("TWA is: " + str(gVars.TrueWindAngle))
   
            if(standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord)):
                self.printedStraight = 0
                #Trying to determine whether 45 degrees clockwise or counter clockwise of TWA wrt North is closer to current heading
                #This means we are trying to determine whether hog-TWA-45 or hog-TWA+45 (both using TWA wrt North) is closer to our current heading.
                #Since those values give us TWA wrt to north, we need to subtract hog from them to get TWA wrt to our heading and figure out which one has a smaller value.
                #To get it wrt to current heading, we use hog-TWA-45-hog and hog-TWA+45-hog.  Both terms have hogs cancelling out.
                #We are left with -TWA-45 and -TWA+45, which makes sense since the original TWA was always with respect to the boat.
                #Since we are trying to figure out which one is closest to turn to, we use absolute values.
                if(self.starboardTackWanted(initialTack)):
                    self.newTackSailing = 1
                    initialTack = None
                    gVars.tacked_flag = 0
                    gVars.logger.info("On starboard tack")

                    while(self.doWeStillWantToTack(self.Dest)):
                        if(gVars.kill_flagPTP == 1):
                          break
                        
                        time.sleep(.1)
                        gVars.tacked_flag = 0
                        self.updateData()

                                               
                        standardcalc.getWeatherSetting(self.sog)                            
                        
                        if(self.isThereChangeToAWAorWeatherOrMode() ):
                            #gVars.logger.info("Changing sheets and rudder")
                            gVars.arduino.adjust_sheets(self.sheetList[abs(int(self.newAWA))][gVars.currentColumn])
                            gVars.arduino.steer(self.AWA_METHOD,-self.TACKING_ANGLE)
                            self.AWA = self.newAWA
                            self.oldColumn = gVars.currentColumn
                            self.tackSailing = self.newTackSailing
                            
                        if(self.newAWA > 0):
                            self.tackDirection = 1
                        else:
                            self.tackDirection = 0
                        
                        self.checkBoundaries()
                        if(gVars.tacked_flag):
                            break
                     
                    if(gVars.tacked_flag == 0):                                                                
                        gVars.arduino.tack(gVars.currentColumn,self.tackDirection)
                        gVars.logger.info("Tacked from 80 degrees")
                    
                elif(self.portTackWanted(initialTack)):
                    self.newTackSailing = 2
                    initialTack = None
                    gVars.tacked_flag = 0
                    gVars.logger.info("On port tack")

                    while(self.doWeStillWantToTack(self.Dest)):
                        if(gVars.kill_flagPTP == 1):
                          break
                        
                        time.sleep(.1)
                        
                        gVars.tacked_flag = 0
                        self.updateData()

                        standardcalc.getWeatherSetting(self.newAWA,self.sog)
                        #TWA = abs(int(TWA))
                        #print ("TWA is: " + str(newTWA))
                        
                        if(self.isThereChangeToAWAorWeatherOrMode()):
                            #gVars.logger.info("Changing sheets and rudder")
                            gVars.arduino.adjust_sheets(self.sheetList[abs(int(self.newAWA))][gVars.currentColumn])
                            gVars.arduino.steer(self.AWA_METHOD,self.TACKING_ANGLE)
                            self.AWA = self.newAWA
                            self.oldColumn = gVars.currentColumn
                            self.tackSailing = self.newTackSailing
                            
                        if(self.newAWA > 0):
                            self.tackDirection = 1
                        else:
                            self.tackDirection = 0
                            
                        self.checkBoundaries()
                        if(gVars.tacked_flag):
                            break
                    
                    if(gVars.tacked_flag == 0):                                                                
                        gVars.arduino.tack(gVars.currentColumn,self.tackDirection)
                        gVars.logger.info("Tacked from 80 degrees")
                    
            else:                    
                if(self.printedStraight == 0):
                    gVars.logger.info("Sailing straight to point")
                    self.printedStraight = 1
                self.newTackSailing = 3
                if(self.isThereChangeToAWAorWeatherOrModeOrAngle()):
                    #gVars.logger.info("Changing sheets and rudder")
                    gVars.arduino.adjust_sheets(self.sheetList[abs(int(self.newAWA))][gVars.currentColumn])
                    gVars.arduino.steer(self.COMPASS_METHOD,self.angleBetweenCoords)
                    self.AWA = self.newAWA
                    self.oldColumn = gVars.currentColumn
                    self.tackSailing = self.newTackSailing
                    self.oldAngleBetweenCoords = self.angleBetweenCoords
                    
                self.checkBoundaries()



        if(gVars.kill_flagPTP == 1):
          gVars.logger.info("PointToPoint is killed")
        else:
          gVars.logger.info("Finished Point to Point")

        return
    
    def updateData(self):
        self.GPSCoord = gVars.currentData.gps_coord
        self.distanceToWaypoint = standardcalc.distBetweenTwoCoords(self.GPSCoord, self.Dest)
        self.newAWA = gVars.currentData.awa
        self.cog = gVars.currentData.cog
        self.hog = gVars.currentData.hog
        self.sog = gVars.currentData.sog * 100
        self.angleBetweenCoords = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
            
    def killPointToPoint(self):
        gVars.kill_flagPTP = 1
        
    def starboardTackWanted(self,initialTack):
        if( (abs(-self.AWA-self.TACKING_ANGLE)<abs(-self.AWA+self.TACKING_ANGLE) and initialTack is None) or initialTack == 1 ):
            return 1
        else:
            return 0
            
    def portTackWanted(self,initialTack):
        if( (abs(self.newAWA-self.TACKING_ANGLE)>=abs(-self.newAWA+self.TACKING_ANGLE) and initialTack is None) or initialTack == 0 ):
            return 1
        else:
            return 0
    
    def doWeStillWantToTack(self):
        if(abs(self.hog-standardcalc.angleBetweenTwoCoords(self.GPSCoord, self.Dest))<80 and gVars.kill_flagPTP ==0):
            return 1
        else:
            return 0
        
    def isThereChangeToAWAorWeatherOrModeOrAngle(self):
        if(self.AWA != self.newAWA or self.oldColumn != gVars.currentColumn or self.tackSailing != self.newTackSailing or abs(self.oldAngleBetweenCoords-self.angleBetweenCoords)>self.ANGLE_CHANGE_THRESHOLD):
            return 1
        else:
            return 0
        
    def isThereChangeToAWAorWeatherOrMode(self):
        if(self.AWA != self.newAWA or self.oldColumn != gVars.currentColumn or self.tackSailing != self.newTackSailing):
            return 1
        else:
            return 0
          
    def checkBoundaries(self):
      for boundary in gVars.boundaries:
        gVars.logger.info("wow")
        if(standardcalc.distBetweenTwoCoords(boundary.coordinate, self.GPSCoord) <= boundary.radius):
          self.sailFromBoundary(boundary)
          break
      return
    
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