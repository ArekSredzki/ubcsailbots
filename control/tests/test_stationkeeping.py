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

class TestAdjustSheetsForExit(unittest.TestCase):
    def setUp(self):
        self.stationKeeping = stationkeeping.StationKeeping()
        self.stationKeeping.secLeft =8
        self.distance = 10
        self.stationKeeping.sheet_percent = 50
        self.sheetMax = 54
    def testTooSlowAndMaxSheeting(self):
        gVars.currentData.sog =.5
        self.assertEqual(self.stationKeeping.adjustSheetsForExit(self.distance,self.sheetMax),54)  
    def testTooFast(self):
        gVars.currentData.sog =1.5
        self.assertEqual(self.stationKeeping.adjustSheetsForExit(self.distance,self.sheetMax),self.stationKeeping.sheet_percent-25)  
    def testJustRight(self):
        gVars.currentData.sog =1
        self.assertEqual(self.stationKeeping.adjustSheetsForExit(self.distance,self.sheetMax),self.stationKeeping.sheet_percent)
      
class TestWaypointCoords(unittest.TestCase):
		def setUp(self):
				self.stationKeeping = stationkeeping.StationKeeping()
				topLeftCoord= datatypes.GPSCoordinate(50,-123)
				topRightCoord=datatypes.GPSCoordinate(50,-122)
				botLeftCoord=datatypes.GPSCoordinate(49,-123)
				botRightCoord=datatypes.GPSCoordinate(49,-122)
				self.boxCoords = standardcalc.setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)  
				self.waypoints = self.stationKeeping.setWayPtCoords(self.boxCoords)
		def testNorthWpt(self):
				northWpt = datatypes.GPSCoordinate(50,-122.5)
				self.assertEqual(self.waypoints[0].lat,northWpt.lat)
				self.assertEqual(round(self.waypoints[0].long,1),northWpt.long)
		def testEastWpt(self):
	  		eastWpt = datatypes.GPSCoordinate(49.5,-122)
	  		self.assertEqual(self.waypoints[1].lat,eastWpt.lat)
		  	self.assertEqual(self.waypoints[1].long,eastWpt.long)     
		def testSouthWpt(self):
				southWpt = datatypes.GPSCoordinate(49,-122.5)
				self.assertEqual(round(self.waypoints[2].long,1),southWpt.long)
				self.assertEqual(self.waypoints[2].lat,southWpt.lat)
		def testWestWpt(self):
	  		eastWpt = datatypes.GPSCoordinate(49.5,-123)
	  		self.assertEqual(self.waypoints[3].lat,eastWpt.lat)
	  		self.assertEqual(self.waypoints[3].long,eastWpt.long)             
	      
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
    def testCalcTackingAngleEquals34(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(10, 20)
        self.assertEquals(round(tackingAngle), 34)
    def testCalcTackingAngleEquals72(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(20, 20)
        self.assertEquals(round(tackingAngle), 72)
    def testCalcTackingAngleEquals91(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(25, 20)
        self.assertEquals(round(tackingAngle), 91)        
    def testCalcTackingAngleEquals110WithHighNum(self):
        tackingAngle = self.stationKeeping.calcTackingAngle(40, 20)
        self.assertEquals(round(tackingAngle), 110)
   
        