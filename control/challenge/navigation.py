'''
Created on Jan 19, 2013

@author: joshandrews
'''
import time
import math
import thread
import sys
sys.path.append("..")
from control.logic import standardcalc
from control.datatype import datatypes
from control import global_vars as gVars
from control import static_vars as sVars
from control.logic import roundbuoy
from control.logic import pointtopoint
from control import sailing_task

# ---    Navigation Challenge    ---
#Input: Buoy GPS Coordinates (Latitude and Longitude of the Buoy), Left Inner Point (The coordinates of the left innermost gate), Right Inner Point (The coordinates of the right innermost gate)
#Output: None
class Navigation(sailing_task.SailingTask):
    LOG_UPDATE_INTERVAL=1
    def __init__(self):
        self.roundbuoy = roundbuoy.RoundBuoy()
        gVars.logger.debug("navigation about to create p2p")
        self.pointtopoint = pointtopoint.PointToPoint()
        gVars.logger.debug("navigation finished create p2p")
        
    def run(self, Waypoint1,Waypoint2,Waypoint3):
        self.nav_log_timer=0
        GPSCoord = gVars.currentData.gps_coord
        
        gVars.kill_flagNav = 0
        
        num_nav_first = 0
        num_nav_start_port = 0
        num_nav_start_stbd = 0
        
        wayList = list()
        
        wayList.append(Waypoint1)
        wayList.append(Waypoint2)
        wayList.append(Waypoint3)
        
        for waypoint in wayList:
            if(waypoint.wtype == "nav_first"):
                BuoyCoords = waypoint.coordinate
                num_nav_first+=1
            elif(waypoint.wtype == "nav_start_port"):
                PortStartInnerPoint = waypoint.coordinate
                num_nav_start_port+=1
            elif(waypoint.wtype == "nav_start_stbd"):
                StarboardStartInnerPoint = waypoint.coordinate
                num_nav_start_stbd+=1
        
        if(num_nav_start_port > 1 or num_nav_start_stbd > 1 or num_nav_first > 1):
            gVars.logger.error("Repeating or too many arguments")
        
        self.interpolatedPoint = standardcalc.returnMidPoint(PortStartInnerPoint,StarboardStartInnerPoint)
        angleOfCourse = standardcalc.angleBetweenTwoCoords(self.interpolatedPoint, BuoyCoords)

        halfwayBackPoint = datatypes.GPSCoordinate((self.interpolatedPoint.lat+BuoyCoords.lat)/2,(self.interpolatedPoint.long+BuoyCoords.long)/2)
        
        gVars.logger.info("Rounding Buoy")                
        if(gVars.kill_flagNav == 0):
            self.roundbuoy.run(BuoyCoords,halfwayBackPoint)
        gVars.logger.info("Heading for Finish")                
        
        if(gVars.kill_flagNav == 0):
            steerByCOG = 1
            acceptDistance = 0.5
            thread.start_new_thread(self.printNavigationLog, ())
            self.pointtopoint.run(self.interpolatedPoint,None,acceptDistance,False, steerByCOG)
        
        return 0
    
    def printNavigationLog(self):
      while (gVars.kill_flagNav == 0):
          if (time.time() - self.nav_log_timer>self.LOG_UPDATE_INTERVAL):
              self.nav_log_timer = time.time()
              gVars.logger.info("Distance: "+ str(standardcalc.distBetweenTwoCoords(gVars.currentData.gps_coord, self.interpolatedPoint)))
      