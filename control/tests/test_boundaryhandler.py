import sys
sys.path.append('..')
import unittest
from control import global_vars as gVars
from control import sailbot_logger
import control.datatype.datatypes as datatypes
from control.logic.boundaries import circleboundaryhandler


class TestBoundaryHandler(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.boundaryHandler = circleboundaryhandler.CircleBoundaryHandler()
        gVars.currentData = datatypes.ArduinoData(0, 1, 2, 3, datatypes.GPSCoordinate(4, 4) , 5, 6, 7, 0, 20)

    def testSetInnerBoundaries(self):   
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49,-123)
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary1 = datatypes.Boundary(coordinate,radius)
        coordinate = datatypes.GPSCoordinate(49,-123.1) #same coordinate
        radius = 50
        boundary2 = datatypes.Boundary(coordinate,radius)
        boundaries = [boundary1, boundary2]
        self.assertEqual(self.boundaryHandler.getInnerBoundaries(boundaries), [boundary1])
        
    def testSetOuterBoundaries(self):
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49,-123.1)
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary1 = datatypes.Boundary(coordinate,radius)
        coordinate = datatypes.GPSCoordinate(49,-123.1) #same coordinate
        radius = 50
        boundary2 = datatypes.Boundary(coordinate,radius)
        boundaries = [boundary1, boundary2]
        self.assertEqual(self.boundaryHandler.getInnerBoundaries(boundaries), [boundary2])
         
    def testInsideHitBoundaries(self):
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49,-123.1)
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries = [boundary]
        self.boundaryHandler.innerBoundaries = self.boundaryHandler.getInnerBoundaries(gVars.boundaries)
        self.boundaryHandler.outerBoundaries = self.boundaryHandler.getOuterBoundaries(gVars.boundaries)
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49,-123)
        self.assertTrue(len(self.boundaryHandler.outerBoundaries) > 0)

        self.assertTrue(self.boundaryHandler.checkOuterBoundaryInterception())
    
    def testOutsideHitBoundaries(self):
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(49,-123)
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123.1) #11ish km west
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries.append(boundary)
        self.boundaryHandler.innerBoundaries = self.boundaryHandler.getInnerBoundaries(gVars.boundaries)
        self.boundaryHandler.outerBoundaries = self.boundaryHandler.getOuterBoundaries(gVars.boundaries)
        
        self.assertFalse(self.boundaryHandler.checkInnerBoundaryInterception())
