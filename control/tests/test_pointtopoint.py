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
        

    def testSetInnerBoundaries(self):   
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        gVars.currentData.gps_coord = self.p2p.GPSCoord
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary1 = datatypes.Boundary(coordinate,radius)
        coordinate = datatypes.GPSCoordinate(49,-123.1) #same coordinate
        radius = 50
        boundary2 = datatypes.Boundary(coordinate,radius)
        boundaries = [boundary1, boundary2]
        self.assertEqual(self.p2p.getInnerBoundaries(boundaries), [boundary1])
        
    def testSetOuterBoundaries(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123.1)
        gVars.currentData.gps_coord = self.p2p.GPSCoord
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary1 = datatypes.Boundary(coordinate,radius)
        coordinate = datatypes.GPSCoordinate(49,-123.1) #same coordinate
        radius = 50
        boundary2 = datatypes.Boundary(coordinate,radius)
        boundaries = [boundary1, boundary2]
        self.assertEqual(self.p2p.getInnerBoundaries(boundaries), [boundary2])
         
    def testCheckHitBoundaries(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123.1)
        gVars.currentData.gps_coord = self.p2p.GPSCoord
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries = [boundary]
        self.p2p.innerBoundaries = self.p2p.getInnerBoundaries(gVars.boundaries)
        self.p2p.outerBoundaries = self.p2p.getOuterBoundaries(gVars.boundaries)
        self.assertTrue(len(self.p2p.outerBoundaries) > 0)
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)

        self.assertTrue(self.p2p.checkOuterBoundaryInterception())
    
    def testOutsideHitBoundaries(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        gVars.currentData.gps_coord = self.p2p.GPSCoord
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123.1) #11ish km west
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries.append(boundary)
        self.p2p.innerBoundaries = self.p2p.getInnerBoundaries(gVars.boundaries)
        self.p2p.outerBoundaries = self.p2p.getOuterBoundaries(gVars.boundaries)
        
        self.assertFalse(self.p2p.checkInnerBoundaryInterception())

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
            
