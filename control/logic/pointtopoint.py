from control.logic import standardcalc
from control import global_vars as gVars
from control import sailing_task
from control.logic.tacking import tackengine
from control.logic.boundaries import circleboundaryhandler
from control.logic import sailor
import time


class PointToPoint(sailing_task.SailingTask):

    ANGLE_CHANGE_THRESHOLD = 5
    ACCEPTANCE_DISTANCE_DEFAULT = 3

    def __init__(self):
        gVars.logger.info("New Point to Point object")
        self.tackEngine = None
        self.boundaryHandler = None
        self.sailor = sailor.Sailor()
          
    def initialize(self):
        gVars.kill_flagPTP = 0
        self.p2pLogger = P2PLogger()
        self.oldAWA = 0
        self.oldColumn = 0
        self.oldAngleBetweenCoords = 0
        if self.boundaryHandler == None:
            self.boundaryHandler = circleboundaryhandler.CircleBoundaryHandler()
        if self.tackEngine == None:
            self.tackEngine = tackengine.TackEngine()       
        if self.acceptDist == None:
            self.acceptDist = self.ACCEPTANCE_DISTANCE_DEFAULT
  

    def withTackEngine(self, tackEngine):
        self.tackEngine = tackEngine
        return self
    def withBoundaryHandler(self, boundaryHandler):
        self.boundaryHandler = boundaryHandler
        return self
      
    def run(self, Dest, acceptDist=None):
        self.acceptDist = acceptDist
        self.initialize()
        gVars.logger.info("Started point to pointAWA toward "+repr(Dest))
        self.Dest = Dest
        self.updateData()

        while(not self.arrivedAtPoint()) and gVars.kill_flagPTP == 0:
            self.updateData()
   
            if(standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord)):
                if(self.tackEngine.onStarboardTack(self.AWA)):
                    self.enterBeatLoop(False)                 
                elif(self.tackEngine.onPortTack(self.AWA)):
                    self.enterBeatLoop(True) 
                    
            else:                    
                self.p2pLogger.printStraight("Sailing straight to point")
                if(self.isThereChangeToAWAorWeatherOrModeOrAngle()):
                    self.sailor.adjustSheetsAndSteerByCompass(self.AWA,self.angleBetweenCoords)                    
            time.sleep(.1)

        self.exitP2P()

    def enterBeatLoop(self, port):
        if port:
            self.p2pLogger.printTacking("On port tack")
            tackAngleMultiplier = -1
        else:
            self.p2pLogger.printTacking("On starboard tack")
            tackAngleMultiplier = 1
           
        while gVars.kill_flagPTP ==0 and not (self.arrivedAtPoint() or self.canLayMarkWithoutTack() ):
            self.updateData()
            bearingToMark = standardcalc.angleBetweenTwoCoords(self.GPSCoord, self.Dest)            
            if self.tackEngine.readyToTack(self.AWA, self.hog, bearingToMark) or self.boundaryHandler.hitBoundary():                
                self.sailor.tack(self.tackEngine.getTackDirection(self.AWA))
                break          
            if self.isThereChangeToAWAorWeatherOrMode():
                self.sailor.adjustSheetsAndSteerByApparentWind(tackAngleMultiplier, self.AWA)
            time.sleep(.1)
                     

    def updateData(self):
        self.GPSCoord = gVars.currentData.gps_coord
        self.distanceToWaypoint = standardcalc.distBetweenTwoCoords(self.GPSCoord, self.Dest)
        self.AWA = gVars.currentData.awa
        self.cog = gVars.currentData.cog
        self.hog = gVars.currentData.hog
        self.sog = gVars.currentData.sog * 100
        self.angleBetweenCoords = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
        standardcalc.updateWeatherSetting(self.AWA,self.sog)

    def arrivedAtPoint(self):
        return self.distanceToWaypoint < self.acceptDist  
       
    def killPointToPoint(self):
        gVars.kill_flagPTP = 1
        

    def isThereChangeToAWAorWeatherOrModeOrAngle(self):
        if(self.AWA != self.oldAWA or self.oldColumn != gVars.currentColumn or abs(self.oldAngleBetweenCoords-self.angleBetweenCoords)>self.ANGLE_CHANGE_THRESHOLD):
            self.updateOldData()
            return 1
        else:
            self.updateOldData()
            return 0

    def isThereChangeToAWAorWeatherOrMode(self):
        if(self.AWA != self.oldAWA or self.oldColumn != gVars.currentColumn):
            self.updateOldData()
            return 1
        else:
            self.updateOldData()
            return 0
             
    def updateOldData(self):
        self.oldAWA = self.AWA
        self.oldColumn = gVars.currentColumn
        self.oldAngleBetweenCoords = self.angleBetweenCoords

            
    def canLayMarkWithoutTack(self):
        if standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord):
            return False
        else:
            windDirection = standardcalc.boundTo180(self.AWA + self.hog)
            bearing = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
            return not standardcalc.isAngleBetween(bearing,windDirection,self.hog)      
    
    def exitP2P(self):
        self.tackEngine = None
        self.boundaryHandler = None
        if(gVars.kill_flagPTP == 1):
            gVars.logger.info("PointToPoint is killed")
        else:
            gVars.logger.info("Finished Point to Point")
            
class P2PLogger:
    def __init__(self):
        self.printedStraight = 0

    def printStraight(self, msg):
        if self.printedStraight == 0:
            gVars.logger.info(msg)
            self.printedStraight = 1
    def printTacking(self, msg):      
        gVars.logger.info(msg)
        self.printedStraight = 0
