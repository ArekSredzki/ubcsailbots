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
        
        