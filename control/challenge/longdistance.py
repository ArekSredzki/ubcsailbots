'''
Created on Jan 19, 2013

@author: joshandrews
'''

import sys
sys.path.append("..")
import control.StaticVars as sVars
from control import GlobalVars as gVars
from control.logic import standardcalc
from control.logic import coresailinglogic

HOG_INDEX=0     # Heading over Ground
COG_INDEX=1     # Course over Ground
SOG_INDEX=2     # Speed over Ground
AWA_INDEX=3     # Apparent Wind Angle Average
GPS_INDEX=4     # GPS Coordinate
SHT_INDEX=5     # Sheet Percentage
SAT_INDEX=6     # GPS Number of Satellites
ACC_INDEX=7     # GPS Accuracy (HDOP)
AUT_INDEX=8     # Auto Mode
RUD_INDEX=9     # Rudder


def run(waypoint1, waypoint2, waypoint3):
    currentData = gVars.currentData
    startPoint = None
    markOne = None
    markTwo = None
   
    wayList = [waypoint1, waypoint2, waypoint3]

    for waypoint in wayList:
        if(waypoint.wtype == sVars.LD_START_FINISH):
            startPoint = waypoint.coordinate
        elif(waypoint.wtype == sVars.LD_FIRST):
            markOne = waypoint.coordinate
        elif(waypoint.wtype == sVars.LD_SECOND):
            markTwo = waypoint.coordinate
    
    ldWaypoints = [markOne, startPoint, markTwo, startPoint, markOne, startPoint, markTwo, startPoint]
    
    for waypoint in ldWaypoints:
        gVars.logger.info("Heading toward " + waypoint + " which is mark " + ldWaypoints.index(waypoint) + " of " + len(ldWaypoints))
        coresailinglogic.pointToPoint(waypoint, None, 20)
        

    return 0