'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import sys
import time
sys.path.append("..")
from datetime import datetime
from control.logic import standardcalc
from control import global_vars as gVars
from control import sailing_task
from control.parser import parsing
from control.datatype import datatypes
from os import path

class StationKeeping(sailing_task.SailingTask):
    
    CHALLENGE_TIME =300
    DISTANCE_TO_EDGE = 15
    AWA_METHOD = 2
    SAIL_BY_APPARENT_WIND_ANGLE_MAX = 110
    SAIL_BY_APPARENT_WIND_ANGLE_MIN = 34
    CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT = 10
    CRITICAL_HEIGHT_BELOW_BOX_MIDPOINT = 5
    CRITICAL_HEIGHT_ABOVE_BOTTOM_OF_BOX = 15
    EXITING_AWA_BEARING = 68 #beam reach
    
    def __init__(self):
        self.upwindWaypoint = 0
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
        self.oldTackingAngle = 0
        self.oldSheet_percent = 0
        self.oldAwa = 0
        self.meanSpd = 0.75   #from old arduino code
        self.secLeft = self.CHALLENGE_TIME
        self.SKLogger = SKLogger()
        self.sheet_percent = 0

    def setWayPtCoords(self, boxCoords): #sets the waypoints of the challenge
        wayPtCoords = []    #order = top face, right face, bottom face, left face
        wayPtCoords.append(standardcalc.returnMidPoint(boxCoords[0],boxCoords[1]))
        wayPtCoords.append(standardcalc.returnMidPoint(boxCoords[1],boxCoords[2]))
        wayPtCoords.append(standardcalc.returnMidPoint(boxCoords[2],boxCoords[3]))
        wayPtCoords.append(standardcalc.returnMidPoint(boxCoords[3],boxCoords[0]))    
        return wayPtCoords
    
    def SKTimer(self):
        gVars.SKMinLeft = ((datetime.now() - gVars.taskStartTime ).seconds) / 60
        gVars.SKSecLeft = ((datetime.now() - gVars.taskStartTime ).seconds) - gVars.SKMinLeft*60
        gVars.SKMilliSecLeft = ((datetime.now() - gVars.taskStartTime).microseconds) / 1000
    
    def getBoxDist(self, boxCoords, absoluteValue=True):
        boxDistList = []  #top, right, bottom, left
        
        TL2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[0]) #top left to boat
        TR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[1]) #top right to boat
        BR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[2]) #bottom right to boat
        BL2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[3]) #bottom left to boat
        
        TL2TR = standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1]) #top left to top right
        TR2BR = standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2]) #top right to bottom right
        BR2BL = standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3]) #bottom right to bottom left
        BL2TL = standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0]) #bottom left to top left
            
            
        topLeftAngle = standardcalc.findCosLawAngle(TL2TR, TL2Boat, TR2Boat)
        topRightAngle = standardcalc.findCosLawAngle(TR2BR, TR2Boat, BR2Boat)
        botRightAngle = standardcalc.findCosLawAngle(BR2BL, BR2Boat, BL2Boat)
        botLeftAngle = standardcalc.findCosLawAngle(BL2TL, BL2Boat, TL2Boat)
        
        topDist = TL2Boat * math.sin(topLeftAngle)
        rightDist = TR2Boat * math.sin(topRightAngle)
        bottomDist = BR2Boat * math.sin(botRightAngle)
        leftDist = BL2Boat * math.sin(botLeftAngle)
        
        if absoluteValue:
            boxDistList = [abs(topDist), abs(rightDist), abs(bottomDist), abs(leftDist)]
        else:
            boxDistList = [topDist, rightDist, bottomDist, leftDist]
            
        return boxDistList
    def getStartDirection(self, wayPtCoords):
      distances=[]
      for i in range(0,4):
        dist = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, wayPtCoords[i])
        distances.append(dist)
      
      direction = (distances.index(min(distances))+2)%4
      return direction
                                                                                            
    def run(self, topLeftWaypnt, topRightWaypnt, botLeftWaypnt, botRightWaypnt):
        
        topLeftCoord = topLeftWaypnt.coordinate
        topRightCoord = topRightWaypnt.coordinate
        botLeftCoord = botLeftWaypnt.coordinate
        botRightCoord = botRightWaypnt.coordinate
        
        boxCoords = standardcalc.setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)   #boxCoords[0] = TL, boxCoords[1] = TR, boxCoords[2] = BR, boxCoords[3] = BL
        wayPtCoords = self.setWayPtCoords(boxCoords)  #top, right, bottom, left
        gVars.logger.info("North waypoint: " + str(wayPtCoords[0]) + " East waypoint: " + str(wayPtCoords[1]) +" South waypoint: " + str(wayPtCoords[2]) + " West waypoint: " + str(wayPtCoords[3]) )
        
        spdList = [self.meanSpd]*100
        boxDistList = self.getBoxDist(boxCoords)  #top, right, bottom, left
        
        self.currentWaypoint = self.getStartDirection(wayPtCoords)
        self.printDistanceLogs(boxDistList)

        gVars.logger.info("------CURRENT WAYPOINT=" + str(self.currentWaypoint)+" ---------")
        gVars.logger.info("Station Keeping Initialization finished. Now running Station Keeping Challenge")
         
        if (gVars.currentData.awa > 0):
            self.upwindWaypoint = (self.currentWaypoint + 1) % 4
        else:
            self.upwindWaypoint = (self.currentWaypoint + 3) % 4
        gVars.logger.info("------UPWIND WAYPOINT=" + str(self.upwindWaypoint)+" ---------")
            
        self.stationKeep(boxCoords, wayPtCoords, spdList)
        
    def stationKeep(self, boxCoords, wayPtCoords, spdList):
        exiting = False
        
        # Gives boat 2 * DISTANCE_TO_EDGE buffer to enter the box (left and right of boundary)
        inTurnZone = True
        turning = True
        
        while ((gVars.kill_flagSK == 0)):
            time.sleep(.1)
            
            self.secLeft = self.CHALLENGE_TIME - (datetime.now() - gVars.taskStartTime).seconds
            self.SKTimer()
            boxDistList = self.getBoxDist(boxCoords)
            self.sailByApparentWind(boxDistList,exiting)
            self.printDistanceLogs(boxDistList)
            if (not exiting):
                if ((boxDistList[self.currentWaypoint] < self.DISTANCE_TO_EDGE) and (inTurnZone == False)):
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("The boat is too close to an edge. Changing current waypoint.")
                    
                    self.currentWaypoint = (self.currentWaypoint + 2) % 4
                    
                    gVars.logger.info("------CURRENT WAYPOINT=" + str(self.currentWaypoint)+" ---------")
                                        
                    if (gVars.currentData.awa > 0):
                        gVars.arduino.gybe(1)
                    else:
                        gVars.arduino.gybe(0)
                        
                    inTurnZone = True
                    turning = True            
                elif ((boxDistList[(self.currentWaypoint+2)%4] > self.DISTANCE_TO_EDGE) and (inTurnZone == True)):
                    gVars.logger.info("Boat out of turn zone, checking for boundaries again. Distance to Edge: " + str(boxDistList[(self.currentWaypoint+2)%4]))
                    
                    inTurnZone = False
                    turning = False
                if (not turning):
                    spdList = standardcalc.changeSpdList(spdList)
                    self.meanSpd = standardcalc.meanOfList(spdList)
                if (boxDistList[self.currentWaypoint] >= self.meanSpd*(self.secLeft+0)):  #leeway of 0 seconds
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 1:" + str(self.meanSpd*(self.secLeft+0)))
                    gVars.logger.info("Seconds Left:" + str(self.secLeft))
                    exiting = True
                    gVars.logger.info("Station Keeping event is about to end. Exiting to current waypoint.")
                elif (boxDistList[(self.currentWaypoint + 2) % 4] >= self.meanSpd*(self.secLeft+0+4) ): #leeway of 0 seconds, 4 seconds for gybe
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 2:" + str(self.meanSpd*(self.secLeft+0+4)))
                    gVars.logger.info("Seconds Left:" + str(self.secLeft))
                    self.currentWaypoint = (self.currentWaypoint + 2) % 4
                    gVars.logger.info("Station Keeping event is about to end. Gybing and exiting to waypoint " + str(self.currentWaypoint))
                    if (gVars.currentData.awa > 0):
                        gVars.arduino.gybe(1)
                    else:
                        gVars.arduino.gybe(0)
                    exiting = True 
            else:
                boxDistListNoAbs = self.getBoxDist(boxCoords, False)
                if boxDistListNoAbs[self.currentWaypoint] < 0 and self.secLeft <= 0:
                    gVars.kill_flagSK = 1;
                
        if (gVars.kill_flagSK == 1):
            gVars.logger.info("Station Keeping Kill Flag initialized. Station Keeping Challenge has been stopped.")
        else:
            gVars.logger.info("Station Keeping Challenge timer has ended.")
        
        boxDistList = self.getBoxDist(boxCoords)
        gVars.SKMinLeft = 0
        gVars.SKSecLeft = 0
        gVars.SKMilliSecLeft = 0
        self.currentWaypoint = None
    
    # StationKeepings sail method.  This function steers and adjusts the sheets
    def sailByApparentWind(self, boxDistList,exiting):
        downwindWaypointIndex = (self.upwindWaypoint+2) % 4
        boxHeight = boxDistList[(self.currentWaypoint+1)%4]+boxDistList[(self.currentWaypoint+3)%4]
        downwindHeight = boxDistList[downwindWaypointIndex]
        downwindHeightIdeal = boxHeight/2

        if (exiting):
            targetAWA = self.EXITING_AWA_BEARING
            self.sheet_percent = self.adjustSheetsForExit(boxDistList[self.currentWaypoint])
        else:           
            targetAWA = self.calcTackingAngle(downwindHeight, downwindHeightIdeal)
            sheetPercentageMultiplier = self.calcDownwindPercent(downwindHeight, downwindHeightIdeal)*.01
            self.sheet_percent =round(sheetPercentageMultiplier*self.sheetList[abs(int(gVars.currentData.awa))][gVars.currentColumn])
        
        windAngleMultiplier = self.calcWindAngleMultiplier()
        targetAWA = windAngleMultiplier*targetAWA

        if (self.isThereChangeInDownwindHeightOrTackingAngleOrAwa(targetAWA)):
            gVars.arduino.adjust_sheets(self.sheet_percent)
            gVars.arduino.steer(self.AWA_METHOD,targetAWA)
            self.printSailingLog(self.sheet_percent,targetAWA)
            self.printHeightLog(downwindHeight,downwindHeightIdeal)

            
    def adjustSheetsForExit(self, distance):
        SHEET_MAX = 54
        MULTIPLIER = 5
        sheet_delta = distance - gVars.currentData.sog*(self.secLeft)
        sheets= self.sheet_percent + sheet_delta*MULTIPLIER
        if sheets<0:
          sheets=0
        elif sheets>SHEET_MAX:
          sheets=SHEET_MAX
        return sheets
           
    def isThereChangeInDownwindHeightOrTackingAngleOrAwa(self, tackingAngle):
        if gVars.currentData.awa != self.oldAwa or tackingAngle != self.oldTackingAngle or self.sheet_percent != self.oldSheet_percent:
            self.updateOldData(tackingAngle)
            return True
        else:
            return False
        
    def updateOldData(self, tackingAngle):
        self.oldTackingAngle = tackingAngle
        self.oldAwa = gVars.currentData.awa
        self.oldSheet_percent = self.sheet_percent
        
    def calcWindAngleMultiplier(self):
        if self.upwindWaypoint == (self.currentWaypoint + 3) % 4:
            return -1
        else:
            return 1
        
    def calcTackingAngle(self, downwindHeight, downwindHeightIdeal):
        if downwindHeight-10 > downwindHeightIdeal:
            return self.SAIL_BY_APPARENT_WIND_ANGLE_MAX
        else:
            return self.SAIL_BY_APPARENT_WIND_ANGLE_MAX - (float(downwindHeightIdeal+10-downwindHeight)/float(downwindHeightIdeal))*(self.SAIL_BY_APPARENT_WIND_ANGLE_MAX-self.SAIL_BY_APPARENT_WIND_ANGLE_MIN)
    
    def calcDownwindPercent(self, downwindHeight, downwindHeightIdeal):
        if downwindHeight-self.CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT > downwindHeightIdeal:
            return 0
        elif downwindHeight-self.CRITICAL_HEIGHT_ABOVE_BOTTOM_OF_BOX > 0:
            return float(downwindHeightIdeal+self.CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT-downwindHeight)/float(downwindHeightIdeal-self.CRITICAL_HEIGHT_BELOW_BOX_MIDPOINT)*100
        else:
            return 100
    
    def printDistanceLogs(self, boxDistList):
        self.SKLogger.distanceLog=(str(int(boxDistList[self.upwindWaypoint]))+" wpt#"+str(self.upwindWaypoint)+ " - Top")+"<br>"
        self.SKLogger.distanceLog+=str(int(boxDistList[(self.upwindWaypoint+3)%4]))+" wpt#"+str((self.upwindWaypoint+3)%4)+" - Left,    "
        self.SKLogger.distanceLog+=str(int(boxDistList[(self.upwindWaypoint+1)%4]))+" wpt#"+str((self.upwindWaypoint+1)%4)+" - Right"+"<br>"
        self.SKLogger.distanceLog+=str(int(boxDistList[(self.upwindWaypoint+2)%4]))+" wpt#"+str((self.upwindWaypoint+2)%4)+" - Bot"
        self.SKLogger.printLog()
    def printHeightLog(self,downwindHeight,downwindHeightIdeal ):
        self.SKLogger.heightLog="HEIGHT:" + str(int(downwindHeight)) +"  Ideal:" + str(int(downwindHeightIdeal))
        self.SKLogger.printLog()
    def printSailingLog(self, sheet_percent, wind_bearing):
        self.SKLogger.sailLog="Sheet Percent:" + str(sheet_percent) +"  Course:" + str(wind_bearing)
        gVars.logger.debug(str(self.meanSpd))
        self.SKLogger.printLog()

class SKLogger:
    LOG_UPDATE_INTERVAL=2
    def __init__(self):
        self.heightLog =''
        self.distanceLog=''
        self.sailLog=''
        self.logTimer =0
    def printLog(self):
      if (time.time() - self.logTimer>self.LOG_UPDATE_INTERVAL):
        self.logTimer = time.time()
        gVars.logger.sklog(self.heightLog)
        gVars.logger.sklog(self.distanceLog)        
        gVars.logger.sklog(self.sailLog)