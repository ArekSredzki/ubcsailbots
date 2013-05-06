'''
Created on May 1, 2013

@author: joshandrews
'''
import unittest
import sys
sys.path.append('..')
from control.challenge import stationkeeping
from control import sailbot_logger
from control import global_vars as gVars
from control.datatype import datatypes
from control.logic import standardcalc

class TestGetStartingDirection(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.stationKeeping = stationkeeping.StationKeeping()
        topLeftCoord= datatypes.GPSCoordinate(50,-123)
        topRightCoord=datatypes.GPSCoordinate(50,-122)
        botLeftCoord=datatypes.GPSCoordinate(49,-123)
        botRightCoord=datatypes.GPSCoordinate(49,-122)
        self.boxCoords = standardcalc.setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)  
        self.waypoints = self.stationKeeping.setWayPtCoords(self.boxCoords)

    def testEnteringFromWest(self):    
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49.4,-123) #west edge
        gVars.currentData.hog = 90
        startDirection = self.stationKeeping.getStartDirection(self.waypoints)
        self.assertEqual(startDirection,1)
    def testEnteringFromEast(self):    
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49.4,-122) #east edge
        gVars.currentData.hog = -90
        startDirection = self.stationKeeping.getStartDirection(self.waypoints)
        self.assertEqual(startDirection,3)

@unittest.skip("skip while testing above code")      
class TestStationKeeping(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.stationKeeping = stationkeeping.StationKeeping()
    # These tests are taken directly from Don's example email.    
    def testCalcDownwindPercent0Percent(self):
        downwindPercent = self.stationKeeping.calcDownwindPercent(30, 20)
        self.assertEquals(downwindPercent,0)
    
    def testCalcDownwindPercent67Percent(self):
        downwindPercent = self.stationKeeping.calcDownwindPercent(20, 20)
        self.assertEquals(round(downwindPercent), 67)
    
    def testCalcDownwindPercent100Percent(self):
        downwindPercent = self.stationKeeping.calcDownwindPercent(15, 20)
        self.assertEquals(round(downwindPercent), 100)
    
    def testCalcDownwindPercent0PercentWithHighNum(self):
        downwindPercent = self.stationKeeping.calcDownwindPercent(40, 20)
        self.assertEquals(downwindPercent,0)
        
    # These tests reflect a proportional awa setting.  Proportions may be changed.
    def testCalcTackingAngleEquals65(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(30, 20)
        self.assertEquals(round(tackingAngle), 65)
    
    def testCalcTackingAngleEquals34(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(15, 20)
        self.assertEquals(round(tackingAngle), 34)
    
    def testCalcTackingAngleEquals48(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(22, 20)
        self.assertEquals(round(tackingAngle), 48)
    
    def testCalcTackingAngleEquals65WithHighNum(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(40, 20)
        self.assertEquals(round(tackingAngle), 65)
        
        