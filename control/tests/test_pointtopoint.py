#Unit tests of standardcalc.py module
import sys, os
sys.path.append(os.path.abspath('../../'))
import unittest
from control import global_vars as gVars
from control.logic import pointtopoint
from control import sailbot_logger
import control.datatype.datatypes as datatypes

class TestPointToPoint(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.p2p = pointtopoint.PointToPoint()

class TestCanLayMarkWithoutTack(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.p2p = pointtopoint.PointToPoint()
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        self.p2p.Dest = datatypes.GPSCoordinate(50,-122) #north east
        self.p2p.sog = 100
    def testCanLayMarkWithoutTack(self):
        self.p2p.AWA = -30
        self.p2p.hog = 30
        self.assertTrue(self.p2p.canLayMarkWithoutTack())
    def testCanNotLayMarkWithoutTack(self):
        self.p2p.AWA = 30
        self.p2p.hog = -30
        self.assertFalse(self.p2p.canLayMarkWithoutTack())
            
