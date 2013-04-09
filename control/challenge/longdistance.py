'''
Created on Jan 19, 2013

@author: joshandrews
'''

import sys
sys.path.append("..")
import control.StaticVars as sVars
from control import GlobalVars as gVars
from control.logic import coresailinglogic

def run(waypoint1, waypoint2, waypoint3):
    startPoint = None
    markOne = None
    markTwo = None
   
    wayList = [waypoint1, waypoint2, waypoint3]
    
    # Sets all waypoints to their appropriate types
    for waypoint in wayList:
        if(waypoint.wtype == sVars.LD_START_FINISH):
            startPoint = waypoint.coordinate
        elif(waypoint.wtype == sVars.LD_FIRST):
            markOne = waypoint.coordinate
        elif(waypoint.wtype == sVars.LD_SECOND):
            markTwo = waypoint.coordinate
    
    ldWaypoints = [markOne, startPoint, markTwo, startPoint, markOne, startPoint, markTwo, startPoint]
    
    for waypoint in ldWaypoints:
        if gVars.kill_flagLD == 0:
            gVars.logger.info("Heading toward " + waypoint.wtype + " which is mark " + str(ldWaypoints.index(waypoint)) + " of " + str(len(ldWaypoints)))
            
            # Startpoint does not require a buoy rounding
            if waypoint != startPoint:
                coresailinglogic.pointToPoint(waypoint, None, 20)
                # Currently will round all buoys port.  May need to be changed for course outline
                coresailinglogic.roundBuoyPort(waypoint)
            else:
                coresailinglogic.pointToPoint(waypoint, None, 3)
                
        else:
            break