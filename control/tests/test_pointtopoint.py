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
      
    def testWhichTackWantedStarboardWanted(self):
        initialTack=None
    
        self.p2p.AWA = 30
        self.assertTrue(self.p2p.starboardTackWanted(initialTack))
        self.assertFalse(self.p2p.portTackWanted(initialTack))
    
        self.p2p.AWA = 150
        self.assertTrue(self.p2p.starboardTackWanted(initialTack))
        self.assertFalse(self.p2p.portTackWanted(initialTack))
    
        self.p2p.AWA = 0
        self.assertTrue(self.p2p.starboardTackWanted(initialTack))
        self.assertFalse(self.p2p.portTackWanted(initialTack))
    def testWhichTackWantedPortWanted(self):
        initialTack=None
        self.p2p.AWA = -30
        self.assertFalse(self.p2p.starboardTackWanted(initialTack))
        self.assertTrue(self.p2p.portTackWanted(initialTack))
        
        self.p2p.AWA = -150
        self.assertFalse(self.p2p.starboardTackWanted(initialTack))
        self.assertTrue(self.p2p.portTackWanted(initialTack))

        
    def testdoWeStillWantToTackReturnTrue(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        self.p2p.Dest = datatypes.GPSCoordinate(49.1,-123) # 0 degrees, N
        self.p2p.tackSailing =1
        self.p2p.roundingLayOffset=0
        self.p2p.hog = 0 # N
        self.assertTrue(self.p2p.doWeStillWantToTack())
        
        self.p2p.hog = 45 # NE
        self.assertTrue(self.p2p.doWeStillWantToTack())
        
        self.p2p.hog = -45 # NW
        self.assertTrue(self.p2p.doWeStillWantToTack())
        
        
    def testdoWeStillWantToTackReturnFalse(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        self.p2p.Dest = datatypes.GPSCoordinate(49.1,-123) # 0 degrees, N
        self.p2p.tackSailing =1
        self.p2p.roundingLayOffset=0
        self.p2p.hog = 90 # E
        self.assertFalse(self.p2p.doWeStillWantToTack())
        
        self.p2p.hog = -90 # NW
        self.assertFalse(self.p2p.doWeStillWantToTack())
        
    def testCheckHitBoundaries(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123) #same coordinate
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries.append(boundary)
        
        self.assertEqual(self.p2p.checkBoundaryInterception(), boundary)
    
    def testOutsideHitBoundaries(self):
        self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
        gVars.boundaries=[]
        coordinate = datatypes.GPSCoordinate(49,-123.1) #11ish km west
        radius = 50
        boundary = datatypes.Boundary(coordinate,radius)
        gVars.boundaries.append(boundary)
        
        self.assertEqual(self.p2p.checkBoundaryInterception(), None)
    
    def testSetTackDirectionToPort(self):
        self.p2p.AWA = 130
        self.p2p.setTackDirection()
        starboard=True
        self.assertEqual(self.p2p.tackDirection, starboard)
    
    def testSetTackDirectionToStarboard(self):
        self.p2p.AWA = -20
        self.p2p.setTackDirection()
        starboard=False
        self.assertEqual(self.p2p.tackDirection, starboard)