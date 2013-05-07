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
from os import path

class StationKeeping(sailing_task.SailingTask):
    
    DISTANCE_TO_EDGE = 15
    AWA_METHOD = 2
    SAIL_BY_APPARENT_WIND_ANGLE_MAX = 120
    SAIL_BY_APPARENT_WIND_ANGLE_MIN = 34
    CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT = 10
    CRITICAL_HEIGHT_BELOW_BOX_MIDPOINT = 5
    CRITICAL_HEIGHT_ABOVE_BOTTOM_OF_BOX = 15
    LOG_UPDATE_INTERVAL=2
    
    def __init__(self):
        self.upwindWaypoint = 0
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
        self.oldTackingAngle = 0
        self.oldSheetPercentageMultiplier = 0
        self.oldAwa = 0
        self.heightLogTime =0
        self.distanceLogTime=0

    def setWayPtCoords(self, boxCoords): #sets the waypoints of the challenge
        wayPtCoords = []    #order = top face, right face, bottom face, left face
        if (boxCoords[0].lat == boxCoords[1].lat):    #square
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[0], standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0, 0))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[1], 0, -(standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[2], -(standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0), 0))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[3], 0, standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0))
        elif (boxCoords[0].lat < boxCoords[1].lat):     #diamond or tilted left square
            cAngle1 = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1])
            midDist1 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.sin(math.radians(cAngle1)) #gets x distance to middle point between TL and TR
            midDist2 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.cos(math.radians(cAngle1)) #gets y distance to middle point between TL and TR
            
            cAngle2 = standardcalc.angleBetweenTwoCoords(boxCoords[1],boxCoords[2]) - 90
            midDist3 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.cos(math.radians(cAngle2)) #gets x distance to middle point between TR and BR
            midDist4 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.sin(math.radians(cAngle2)) #gets y distance to middle point between TT and BR
            
            cAngle3 = 180 - math.fabs(standardcalc.angleBetweenTwoCoords(boxCoords[2],boxCoords[3]))
            midDist5 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.sin(math.radians(cAngle3)) #gets x distance to middle point between BR and BL
            midDist6 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.cos(math.radians(cAngle3)) #gets y distance to middle point between BR and BL
            
            cAngle4 = 90 - abs(standardcalc.angleBetweenTwoCoords(boxCoords[3],boxCoords[0]))
            midDist7 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.cos(math.radians(cAngle4)) #gets x distance to middle point between BL and TL
            midDist8 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.sin(math.radians(cAngle4)) #gets y distance to middle point between BL and TL
            
            topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, midDist2)
            rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], midDist3, -midDist4)
            botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist5, -midDist6)
            leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], -midDist7, midDist8)
            
            wayPtCoords.append(topMidpnt)
            wayPtCoords.append(rightMidpnt)
            wayPtCoords.append(botMidpnt)
            wayPtCoords.append(leftMidpnt)
            
            gVars.logger.info("cAngle4: " + str(cAngle4) + "Midpoint1: " + str(topMidpnt) + " Midpoint2: " + str(rightMidpnt) + " Midpoint3: " + str(botMidpnt) + " Midpoint4: " + str(leftMidpnt))
        else:    #right tilted square
            cAngle1 = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1]) - 90
            midDist1 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.cos(math.radians(cAngle1)) #gets x distance to middle point between TL and TR
            midDist2 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.sin(math.radians(cAngle1)) #gets y distance to middle point between TL and TR
            
            cAngle2 = 180 - abs(standardcalc.angleBetweenTwoCoords(boxCoords[1],boxCoords[2]))
            midDist3 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.sin(math.radians(cAngle2)) #gets x distance to middle point between TR and BR
            midDist4 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.cos(math.radians(cAngle2)) #gets y distance to middle point between TT and BR
            
            cAngle3 = 90 - abs(math.fabs(standardcalc.angleBetweenTwoCoords(boxCoords[2],boxCoords[3])))
            midDist5 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.cos(math.radians(cAngle3)) #gets x distance to middle point between BR and BL
            midDist6 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.sin(math.radians(cAngle3)) #gets y distance to middle point between BR and BL
            
            cAngle4 = standardcalc.angleBetweenTwoCoords(boxCoords[3],boxCoords[0])
            midDist7 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.sin(math.radians(cAngle4)) #gets x distance to middle point between BL and TL
            midDist8 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.cos(math.radians(cAngle4)) #gets y distance to middle point between BL and TL
            
            topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, -midDist2)
            rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], -midDist2, -midDist1)
            botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist1, midDist2)
            leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], midDist2, midDist1)
            
            wayPtCoords.append(topMidpnt)
            wayPtCoords.append(rightMidpnt)
            wayPtCoords.append(botMidpnt)
            wayPtCoords.append(leftMidpnt)
            
            gVars.logger.info("cAngle4: " + str(cAngle4) + "Midpoint1: " + str(topMidpnt) + " Midpoint2: " + str(rightMidpnt) + " Midpoint3: " + str(botMidpnt) + " Midpoint4: " + str(leftMidpnt))
        
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
        
        spdList = [0.75]*100
        boxDistList = self.getBoxDist(boxCoords)  #top, right, bottom, left
        
        meanSpd = 0.75   #from old arduino code
        self.currentWaypoint = self.getStartDirection(wayPtCoords)
        self.printDistanceLogs(boxDistList)

        gVars.logger.info("The current waypoint is " + str(self.currentWaypoint) + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
        gVars.logger.info("Station Keeping Initialization finished. Now running Station Keeping Challenge")
         
        if (gVars.currentData.awa > 0):
            self.upwindWaypoint = (self.currentWaypoint + 3) % 4
        else:
            self.upwindWaypoint = (self.currentWaypoint + 1) % 4
            
        self.stationKeep(boxCoords, wayPtCoords, spdList, meanSpd)
        
    def stationKeep(self, boxCoords, wayPtCoords, spdList, meanSpd):
        exiting = False
        
        # Gives boat 2 * DISTANCE_TO_EDGE buffer to enter the box (left and right of boundary)
        inTurnZone = True
        turning = True
        
        while ((gVars.kill_flagSK == 0)):
            time.sleep(.1)
            
            secLeft = 300 - (datetime.now() - gVars.taskStartTime).seconds
            self.SKTimer()
            boxDistList = self.getBoxDist(boxCoords)
            self.sailByApparentWind(boxDistList)
            self.printDistanceLogs(boxDistList)
            if (not exiting):
                if ((boxDistList[self.currentWaypoint] < self.DISTANCE_TO_EDGE) and (inTurnZone == False)):
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("The boat is too close to an edge. Changing current waypoint.")
                    
                    self.currentWaypoint = (self.currentWaypoint + 2) % 4
                    
                    gVars.logger.info("The current waypoint is " + str(self.currentWaypoint) + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
                    gVars.logger.info("Commencing gybe.")
                    
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
                    meanSpd = standardcalc.meanOfList(spdList)
                if (boxDistList[self.currentWaypoint] >= meanSpd*(secLeft+0)):  #leeway of 0 seconds
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 1:" + str(meanSpd*(secLeft+0)))
                    gVars.logger.info("Seconds Left:" + str(secLeft))
                    exiting = True
                    gVars.logger.info("Station Keeping event is about to end. Exiting to current waypoint.")
                elif (boxDistList[(self.currentWaypoint + 2) % 4] >= meanSpd*(secLeft+0+4) ): #leeway of 0 seconds, 4 seconds for gybe
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 2:" + str(meanSpd*(secLeft+0+4)))
                    gVars.logger.info("Seconds Left:" + str(secLeft))
                    self.currentWaypoint = (self.currentWaypoint + 2) % 4
                    gVars.logger.info("Station Keeping event is about to end. Gybing and exiting to waypoint " + str(self.currentWaypoint))
                    if (gVars.currentData.awa > 0):
                        gVars.arduino.gybe(1)
                    else:
                        gVars.arduino.gybe(0)
                    exiting = True 
            else:
                boxDistListNoAbs = self.getBoxDist(boxCoords, False)
                if boxDistListNoAbs[self.currentWaypoint] < 0 and secLeft <= 0:
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
    def sailByApparentWind(self, boxDistList):
        downwindWaypointIndex = (self.upwindWaypoint+2) % 4
        boxHeight = boxDistList[(self.currentWaypoint+1)%4]+boxDistList[(self.currentWaypoint+3)%4]
        downwindHeight = boxDistList[downwindWaypointIndex]
        downwindHeightIdeal = boxHeight/2
        self.printHeightLog(downwindHeight,downwindHeightIdeal)
        
        tackAngleMultiplier = self.calcTackAngleMultiplier()
        tackingAngle = self.calcTackingAngle(downwindHeight, downwindHeightIdeal)
        sheetPercentageMultiplier = self.calcDownwindPercent(downwindHeight, downwindHeightIdeal)*.01
        
        if (self.isThereChangeInDownwindHeightOrTackingAngleOrAwa(tackingAngle, sheetPercentageMultiplier)):
            gVars.arduino.adjust_sheets(round(sheetPercentageMultiplier*self.sheetList[abs(int(gVars.currentData.awa))][gVars.currentColumn]))
            gVars.arduino.steer(self.AWA_METHOD,tackAngleMultiplier*tackingAngle)
    
    def isThereChangeInDownwindHeightOrTackingAngleOrAwa(self, tackingAngle, sheetPercentageMultiplier):
        if gVars.currentData.awa != self.oldAwa or tackingAngle != self.oldTackingAngle or sheetPercentageMultiplier != self.oldSheetPercentageMultiplier:
            self.updateOldData(tackingAngle, sheetPercentageMultiplier)
            return True
        else:
            return False
        
    def updateOldData(self, tackingAngle, sheetPercentageMultiplier):
        self.oldTackingAngle = tackingAngle
        self.oldAwa = gVars.currentData.awa
        self.oldSheetPercentageMultiplier = sheetPercentageMultiplier
        
    def calcTackAngleMultiplier(self):
        if self.upwindWaypoint == (self.currentWaypoint + 3) % 4:
            return 1
        else:
            return -1
        
    def calcTackingAngle(self, downwindHeight, downwindHeightIdeal):
        if downwindHeight-10 > downwindHeightIdeal:
            return self.SAIL_BY_APPARENT_WIND_ANGLE_MAX
        else:
            return self.SAIL_BY_APPARENT_WIND_ANGLE_MAX - (float(downwindHeightIdeal+10-downwindHeight)/float(downwindHeightIdeal-5))*(self.SAIL_BY_APPARENT_WIND_ANGLE_MAX-self.SAIL_BY_APPARENT_WIND_ANGLE_MIN)
    
    def calcDownwindPercent(self, downwindHeight, downwindHeightIdeal):
        if downwindHeight-self.CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT > downwindHeightIdeal:
            return 0
        elif downwindHeight-self.CRITICAL_HEIGHT_ABOVE_BOTTOM_OF_BOX > 0:
            return float(downwindHeightIdeal+self.CRITICAL_HEIGHT_ABOVE_BOX_MIDPOINT-downwindHeight)/float(downwindHeightIdeal-self.CRITICAL_HEIGHT_BELOW_BOX_MIDPOINT)*100
        else:
            return 100
    def printDistanceLogs(self, boxDistList):
      if (time.time()-self.distanceLogTime >self.LOG_UPDATE_INTERVAL):
        self.distanceLogTime = time.time()
        gVars.logger.info(str(int(boxDistList[0]))+" - Top dist  ")
        gVars.logger.info(str(int(boxDistList[1]))+" - Right Dist: ")
        gVars.logger.info(str(int(boxDistList[2]))+" - Bot Dist: ")
        gVars.logger.info(str(int(boxDistList[3]))+" - Left Dist: ")
    def printHeightLog(self,downwindHeight,downwindHeightIdeal ):
      if (time.time()-self.heightLogTime >self.LOG_UPDATE_INTERVAL):
        self.heightLogTime = time.time()
        gVars.logger.info("HEIGHT: " + str(int(downwindHeight)) +"  Ideal Height: " + str(int(downwindHeightIdeal)) )
