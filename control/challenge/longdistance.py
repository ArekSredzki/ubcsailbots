'''
Created on Jan 19, 2013

@author: joshandrews
'''

import sys
sys.path.append("..")
from control import static_vars as sVars
from control import global_vars as gVars
from control.logic import pointtopoint
from control.logic import roundbuoy
from control import sailing_task

class LongDistance(sailing_task.SailingTask):
    
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint()
        self.roundbuoy = roundbuoy.RoundBuoy()
    
    def run(self, waypoint1, waypoint2, waypoint3):
        startPoint = None
        markOne = None
        markTwo = None
       
        wayList = [waypoint1, waypoint2, waypoint3]
        
        # Sets all waypoints to their appropriate types
        for waypoint in wayList:
            if(waypoint.wtype == sVars.LD_START_FINISH):
                startPoint = waypoint
            elif(waypoint.wtype == sVars.LD_FIRST):
                markOne = waypoint
            elif(waypoint.wtype == sVars.LD_SECOND):
                markTwo = waypoint
        
        ldWaypoints = [markOne, startPoint, markTwo, startPoint, markOne, startPoint, markTwo, startPoint, markOne]
        
        for waypoint in ldWaypoints:
            if gVars.kill_flagLD == 0:
                gVars.logger.info("Heading toward " + waypoint.wtype + " which is mark " + str(ldWaypoints.index(waypoint)) + " of " + str(len(ldWaypoints)))
                
                # Startpoint does not require a buoy rounding
                if waypoint.coordinate != startPoint.coordinate:
                    self.pointtopoint.run(waypoint.coordinate, None, 30)
                    # Currently will round all buoys port.  May need to be changed for course outline
                    self.roundbuoy.run(waypoint.coordinate)
                else:
                    self.pointtopoint.run(waypoint.coordinate, None, 10)
                    
            else:
                break