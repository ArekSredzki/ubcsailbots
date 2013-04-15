'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import sys
import thread
import time
sys.path.append("..")
from datetime import datetime
from control.logic import standardcalc
from control.logic import pointtopoint
import control.GlobalVars as gVars
from control import sailingtask

class StationKeeping(sailingtask.SailingTask):
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint()
        
    def setWayPtCoords(self, boxCoords): #sets the waypoints of the challenge
        wayPtCoords = []    #order = top face, right face, bottom face, left face
        if (boxCoords[0].lat == boxCoords[1].lat):    #square
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[0], standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0, 100.0))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[1], 100.0, -(standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[2], -(standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0), -100.0))
            wayPtCoords.append(standardcalc.GPSDistAway(boxCoords[3], -100.0, standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0))
        elif (boxCoords[0].lat < boxCoords[1].lat):     #diamond or tilted left square
            cAngle1 = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1])
            wayPntDist1 = 100.0*math.sin(90 - cAngle1) #x
            wayPntDist2 = 100.0*math.cos(90 - cAngle1) #y
            midDist1 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.sin(cAngle1) #gets x distance to middle point between TL and TR
            midDist2 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.cos(cAngle1) #gets y distance to middle point between TL and TR
            
            cAngle2 = standardcalc.angleBetweenTwoCoords(boxCoords[1],boxCoords[2]) - 90
            wayPntDist3 = 100.0*math.cos(90 - cAngle2) #x
            wayPntDist4 = 100.0*math.sin(90 - cAngle2) #y
            midDist3 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.cos(cAngle2) #gets x distance to middle point between TR and BR
            midDist4 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.sin(cAngle2) #gets y distance to middle point between TT and BR
            
            cAngle3 = 180 - math.fabs(standardcalc.angleBetweenTwoCoords(boxCoords[2],boxCoords[3]))
            wayPntDist5 = 100.0*math.sin(90 - cAngle3) #x
            wayPntDist6 = 100.0*math.cos(90 - cAngle3) #y
            midDist5 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.sin(cAngle3) #gets x distance to middle point between BR and BL
            midDist6 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.cos(cAngle3) #gets y distance to middle point between BR and BL
            
            cAngle4 = 90 - standardcalc.angleBetweenTwoCoords(boxCoords[3],boxCoords[0])
            wayPntDist7 = 100.0*math.cos(90 - cAngle4)
            wayPntDist8 = 100.0*math.sin(90 - cAngle4)
            midDist7 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.cos(cAngle4) #gets x distance to middle point between BL and TL
            midDist8 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.sin(cAngle4) #gets y distance to middle point between BL and TL
            
            topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, midDist2)
            rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], midDist3, -midDist4)
            botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist5, -midDist6)
            leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], -midDist7, midDist8)
            wayPtCoords.append(standardcalc.GPSDistAway(topMidpnt, -wayPntDist1, wayPntDist2))
            wayPtCoords.append(standardcalc.GPSDistAway(rightMidpnt, wayPntDist3, wayPntDist4))
            wayPtCoords.append(standardcalc.GPSDistAway(botMidpnt, wayPntDist5, -wayPntDist6))
            wayPtCoords.append(standardcalc.GPSDistAway(leftMidpnt, -wayPntDist7, -wayPntDist8))
        else:    #right tilted square
            cAngle1 = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1]) - 90
            wayPntDist1 = 100.0*math.cos(90 - cAngle1) #x
            wayPntDist2 = 100.0*math.sin(90 - cAngle1) #y
            midDist1 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.cos(cAngle1) #gets x distance to middle point between TL and TR
            midDist2 = (standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1])/2.0)*math.sin(cAngle1) #gets y distance to middle point between TL and TR
            
            cAngle2 = 180 - standardcalc.angleBetweenTwoCoords(boxCoords[1],boxCoords[2])
            wayPntDist3 = 100.0*math.sin(90 - cAngle2) #x
            wayPntDist4 = 100.0*math.cos(90 - cAngle2) #y
            midDist3 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.sin(cAngle2) #gets x distance to middle point between TR and BR
            midDist4 = (standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2])/2.0)*math.cos(cAngle2) #gets y distance to middle point between TT and BR
            
            cAngle3 = 90 - math.fabs(standardcalc.angleBetweenTwoCoords(boxCoords[2],boxCoords[3]))
            wayPntDist5 = 100.0*math.cos(90 - cAngle3) #x
            wayPntDist6 = 100.0*math.sin(90 - cAngle3) #y
            midDist5 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.cos(cAngle3) #gets x distance to middle point between BR and BL
            midDist6 = (standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3])/2.0)*math.sin(cAngle3) #gets y distance to middle point between BR and BL
            
            cAngle4 = standardcalc.angleBetweenTwoCoords(boxCoords[3],boxCoords[0])
            wayPntDist7 = 100.0*math.sin(90 - cAngle4)
            wayPntDist8 = 100.0*math.cos(90 - cAngle4)
            midDist7 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.sin(cAngle4) #gets x distance to middle point between BL and TL
            midDist8 = (standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0])/2.0)*math.cos(cAngle4) #gets y distance to middle point between BL and TL
            
            topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, -midDist2)
            rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], -midDist2, -midDist1)
            botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist1, midDist2)
            leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], midDist2, midDist1)
            wayPtCoords.append(standardcalc.GPSDistAway(topMidpnt, wayPntDist1, wayPntDist2))
            wayPtCoords.append(standardcalc.GPSDistAway(rightMidpnt, wayPntDist2, -wayPntDist1))
            wayPtCoords.append(standardcalc.GPSDistAway(botMidpnt, -wayPntDist1, -wayPntDist2))
            wayPtCoords.append(standardcalc.GPSDistAway(leftMidpnt, -wayPntDist2, wayPntDist1))
            
        return wayPtCoords
    
    
    def SKTimer(self):
        gVars.SKMinLeft = ((datetime.now() - gVars.taskStartTime ).seconds) / 60
        gVars.SKSecLeft = ((datetime.now() - gVars.taskStartTime ).seconds) - gVars.SKMinLeft*60
        gVars.SKMilliSecLeft = ((datetime.now() - gVars.taskStartTime).microseconds) / 1000
    
    def getBoxDist(self, boxCoords):
        boxDistList = []  #top, right, bottom, left
        TL2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[0]) #top left to boat
        TR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[1]) #top right to boat
        BR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[2]) #bottom right to boat
        BL2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, boxCoords[3]) #bottom left to boat
        TL2TR = standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1]) #top left to top right
        TR2BR = standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2]) #top right to bottom right
        BR2BL = standardcalc.distBetweenTwoCoords(boxCoords[2], boxCoords[3]) #bottom right to bottom left
        BL2TL = standardcalc.distBetweenTwoCoords(boxCoords[3], boxCoords[0]) #bottom left to top left
            
        #gVars.logger.info("TL2Boat: " + str(TL2Boat)+ " TR2Boat: " + str(TR2Boat)+ " BR2Boat: " + str(BR2Boat)+ " BL2Boat: " + str(BL2Boat)+ " TL2TR: " + str(TL2TR)+ " TR2BR: " + str(TR2BR)+ " BR2BL: " + str(BR2BL)+ " BL2TL: " + str(BL2TL))
            
        topLeftAngle = standardcalc.findCosLawAngle(TL2TR, TL2Boat, TR2Boat)
        topRightAngle = standardcalc.findCosLawAngle(TR2BR, TR2Boat, BR2Boat)
        botRightAngle = standardcalc.findCosLawAngle(BR2BL, BR2Boat, BL2Boat)
        botLeftAngle = standardcalc.findCosLawAngle(BL2TL, BL2Boat, TL2Boat)
        
        boxDistList.append( abs(TL2Boat * math.sin(topLeftAngle)) )  #top dist
        boxDistList.append( abs(TR2Boat * math.sin(topRightAngle)) )  #right dist
        boxDistList.append( abs(BR2Boat * math.sin(botRightAngle)) ) #bottom dist
        boxDistList.append( abs(BL2Boat * math.sin(botLeftAngle)) ) #left dist
        #gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
        return boxDistList
    
    def run(self, topLeftWaypnt, topRightWaypnt, botLeftWaypnt, botRightWaypnt):
        topLeftCoord = topLeftWaypnt.coordinate
        topRightCoord = topRightWaypnt.coordinate
        botLeftCoord = botLeftWaypnt.coordinate
        botRightCoord = botRightWaypnt.coordinate
        boxCoords = standardcalc.setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)   #boxCoords[0] = TL, boxCoords[1] = TR, boxCoords[2] = BR, boxCoords[3] = BL
        wayPtCoords = self.setWayPtCoords(boxCoords)  #top, right, bottom, left
        gVars.logger.info("North waypoint: " + str(wayPtCoords[0]) + " East waypoint: " + str(wayPtCoords[1]) +" South waypoint: " + str(wayPtCoords[2]) + " West waypoint: " + str(wayPtCoords[3]) )
        spdList = [0.75]*10
        boxDistList = self.getBoxDist(boxCoords)  #top, right, bottom, left
        meanSpd = 0.75   #from old arduino code
        gVars.SKCurrentWaypnt = boxDistList.index(min(boxDistList))
        thread.start_new_thread(self.pointtopoint.run, (wayPtCoords[gVars.SKCurrentWaypnt], ))
        gVars.logger.info("The current waypoint is " + str(gVars.SKCurrentWaypnt) + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
        gVars.logger.info("Station Keeping Initialization finished. Now running Station Keeping Challenge")
        self.skrun(boxCoords, wayPtCoords, spdList, meanSpd)
        return
        
    def skrun(self, boxCoords, wayPtCoords, spdList, meanSpd):
        exiting = 0
        inTurnZone = 0
        turning = 0
        while (((datetime.now() - gVars.taskStartTime).seconds < 300) and (gVars.kill_flagSK == 0)):
            time.sleep(.1)
            secLeft = 300 - (datetime.now() - gVars.taskStartTime).seconds
            #gVars.logger.info("Time left is " + str(secLeft) +" seconds.")
            self.SKTimer()
            boxDistList = self.getBoxDist(boxCoords)
            if (exiting == 0):
                #gVars.logger.info("WPNSTUFF. Current waypoint lat: " + str(wayPtCoords[gVars.SKCurrentWaypnt].lat) + ". Current waypoint long: " + str(wayPtCoords[gVars.SKCurrentWaypnt].long) + ". current GPS lat: " + str(gVars.currentData.gps_coord.lat) + ". current GPS long: " + str(gVars.currentData.gps_coord.long))
                if (standardcalc.isWPNoGoAWA(gVars.currentData.awa,gVars.currentData.hog, wayPtCoords[gVars.SKCurrentWaypnt], gVars.currentData.sog, gVars.currentData.gps_coord)):
                    gVars.logger.info("The boat is sailing upwind. Changing current waypoint.")
                    gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 1) % 4
                    gVars.logger.info("The current waypoint is " + str(gVars.SKCurrentWaypnt) + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
                    gVars.kill_flagPTP = 1
                    thread.start_new_thread(self.pointtopoint.run, (wayPtCoords[gVars.SKCurrentWaypnt], ))
                    turning = 1
                if (((boxDistList[0] < 10) or (boxDistList[1] < 10) or (boxDistList[2] < 10) or (boxDistList[3] < 10)) and (inTurnZone == 0)):
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("The boat is too close to an edge. Changing current waypoint.")
                    gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
                    gVars.logger.info("The current waypoint is " + str(gVars.SKCurrentWaypnt) + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
                    gVars.kill_flagPTP = 1
                    gVars.logger.info("Commencing gybe.")
                    if (gVars.currentData.awa < 0):
                        gVars.arduino.gybe(1)
                    else:
                        gVars.arduino.gybe(0)
                    thread.start_new_thread(self.pointtopoint.run, (wayPtCoords[gVars.SKCurrentWaypnt], ))
                    inTurnZone = 1
                    turning = 1
                elif ((boxDistList[(gVars.SKCurrentWaypnt+2)%4] > 10) and (inTurnZone == 1)):
                    inTurnZone = 0
                    turning = 0
                if (turning == 0):
                    spdList = standardcalc.changeSpdList(spdList)
                    meanSpd = standardcalc.meanOfList(spdList)
                    #gVars.logger.info("The mean speed of the boat is " + str(meanSpd) + " metres per second.")
                if (boxDistList[gVars.SKCurrentWaypnt] >= meanSpd*(secLeft+2)):  #leeway of 2 seconds
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 1:" + str(meanSpd*(secLeft+2)))
                    exiting = 1
                    gVars.logger.info("Station Keeping event is about to end. Exiting to current waypoint.")
                elif (boxDistList[(gVars.SKCurrentWaypnt + 2) % 4] >= meanSpd*(secLeft+2+4) ): #leeway of 2 seconds, 4 seconds for gybe
                    gVars.logger.info("distances: N: " + str(boxDistList[0]) + " E: " + str(boxDistList[1]) + " S: " + str(boxDistList[2]) + " W: " + str(boxDistList[3]))
                    gVars.logger.info("Distance left to travel 2:" + str(meanSpd*(secLeft+2+4)))
                    gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
                    gVars.kill_flagPTP = 1
                    gVars.logger.info("Station Keeping event is about to end. Gybing and exiting to waypoint " + str(gVars.SKCurrentWaypnt))
                    if (gVars.currentData.awa < 0):
                        gVars.arduino.gybe(1)
                    else:
                        gVars.arduino.gybe(0)
                    thread.start_new_thread(self.pointtopoint.run, (wayPtCoords[gVars.SKCurrentWaypnt], ))
                    exiting = 1
        if (gVars.kill_flagSK == 1):
            gVars.logger.info("Station Keeping Kill Flag initialized. Station Keeping Challenge has been stopped.")
        else:
            gVars.logger.info("Station Keeping Challenge timer has ended.")
        boxDistList = self.getBoxDist(boxCoords)
        gVars.SKMinLeft = 0
        gVars.SKSecLeft = 0
        gVars.SKMilliSecLeft = 0
        gVars.kill_flagSK = 0
        gVars.SKCurrentWaypnt = None
