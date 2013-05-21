#Unit tests of standardcalc.py module
import sys
sys.path.append('..')
import unittest
from control import global_vars as gVars
from control import sailbot_logger
import control.datatype.datatypes as datatypes
from control.logic.tacking import tackengine
from control.logic.tacking import roundingtackengine
from control.logic import standardcalc


class TestTackEngine(unittest.TestCase):
    def setUp(self):
        self.tackengine = tackengine.TackEngine()
        gVars.logger = sailbot_logger.Logger()

    def testWhichTackWantedStarboardWanted(self):
    
        AWA = 30
        self.assertTrue(self.tackengine.onStarboardTack(AWA))
        self.assertFalse(self.tackengine.onPortTack(AWA))
    
        AWA = 150
        self.assertTrue(self.tackengine.onStarboardTack(AWA))
        self.assertFalse(self.tackengine.onPortTack(AWA))
    
        AWA = 0
        self.assertTrue(self.tackengine.onStarboardTack(AWA))
        self.assertFalse(self.tackengine.onPortTack(AWA))
    def testWhichTackWantedPortWanted(self):
        AWA = -30
        self.assertFalse(self.tackengine.onStarboardTack(AWA))
        self.assertTrue(self.tackengine.onPortTack(AWA))
        
        AWA = -150
        self.assertFalse(self.tackengine.onStarboardTack(AWA))
        self.assertTrue(self.tackengine.onPortTack(AWA))

        
    def testReadyToTackFalse(self):
        AWA =30      
        GPSCoord = datatypes.GPSCoordinate(49,-123)
        Dest = datatypes.GPSCoordinate(49.1,-123) # 0 degrees, N
        bearingToMark = standardcalc.angleBetweenTwoCoords(GPSCoord, Dest)            
        hog = 0 # N
        self.assertFalse(self.tackengine.readyToTack(AWA, hog, bearingToMark))
        
        hog = 45 # NE
        self.assertFalse(self.tackengine.readyToTack(AWA, hog, bearingToMark))
        
        hog = -45 # NW
        self.assertFalse(self.tackengine.readyToTack(AWA, hog, bearingToMark))
        
        
    def testReadyToTackFalse(self):
        AWA =30      
        GPSCoord = datatypes.GPSCoordinate(49,-123)
        Dest = datatypes.GPSCoordinate(49.1,-123) # 0 degrees, N
        bearingToMark = standardcalc.angleBetweenTwoCoords(GPSCoord, Dest)            
        hog = 90 # E
        self.assertTrue(self.tackengine.readyToTack(AWA, hog, bearingToMark))
        
        hog = -90 # NW
        self.assertTrue(self.tackengine.readyToTack(AWA, hog, bearingToMark))
    
        
    def testSetTackDirectionToPort(self):
        AWA = 130
        port=1
        self.assertEqual(self.tackengine.getTackDirection(AWA), port)
    
    def testSetTackDirectionToStarboard(self):
        AWA = -20
        starboard=0
        self.assertEqual(self.tackengine.getTackDirection(AWA), starboard)

class TestRoundingTackEngine(unittest.TestCase):
    def setUp(self):
        self.tackengine = roundingtackengine.RoundingTackEngine("starboard")
        gVars.logger = sailbot_logger.Logger()
    
    def testWhichTackWantedStarboardWanted(self):
    
        AWA = 0
        self.tackengine.initialTack = "starboard"
        self.assertTrue(self.tackengine.onStarboardTack(AWA))
        self.assertFalse(self.tackengine.onPortTack(AWA))

    def testWhichTackWantedPortWanted(self):
        AWA = 0
        self.tackengine.initialTack = "port"
        self.assertTrue(self.tackengine.onStarboardTack(AWA))
        self.assertFalse(self.tackengine.onPortTack(AWA))
    
    def testLayAngle90(self):
        self.tackengine.rounding ="starboard"
        self.tackengine.currentTack = "starboard"
        self.assertEqual(self.tackengine.layAngle, 90)
        
        self.tackengine.rounding ="port"
        self.tackengine.currentTack = "port"
        self.assertEqual(self.tackengine.layAngle, 90)

    def testLayAngle45(self):
        self.tackengine.rounding ="starboard"
        self.tackengine.currentTack = "port"
        self.assertEqual(self.tackengine.layAngle, 45)
        
        self.tackengine.rounding ="port"
        self.tackengine.currentTack = "starboard"
        self.assertEqual(self.tackengine.layAngle, 45)

                