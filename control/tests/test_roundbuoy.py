import sys
sys.path.append('..')
import unittest
from control import global_vars as gVars
from control.logic import roundbuoy
from control.logic import standardcalc
from control import sailbot_logger
from control.datatype import datatypes

class TestRoundBuoy(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.round_buoy = roundbuoy.RoundBuoy()
        gVars.currentData = datatypes.ArduinoData(0, 0, 0,
                          0, datatypes.GPSCoordinate(0, 0), 0, 
                          0, 0, 0, 0)
        self.buoyLoc = datatypes.GPSCoordinate(1,1)
        self.angleBetweenBuoyAndGPSCoord = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, self.buoyLoc)        
        
    def testFindRightBuoyPoint(self):        
        rightBuoyPoint = roundbuoy.RoundBuoy.findRightBuoyPoint(self.round_buoy, self.buoyLoc)
        self.assertTrue(abs(standardcalc.angleBetweenTwoCoords(self.buoyLoc,rightBuoyPoint)-(self.angleBetweenBuoyAndGPSCoord+roundbuoy.RoundBuoy.TargetAndBuoyAngle))<0.1)
        
    def testFindLeftBuoyPoint(self):
        leftBuoyPoint = roundbuoy.RoundBuoy.findLeftBuoyPoint(self.round_buoy, self.buoyLoc)
        self.assertTrue(abs(standardcalc.angleBetweenTwoCoords(self.buoyLoc,leftBuoyPoint)-(self.angleBetweenBuoyAndGPSCoord-roundbuoy.RoundBuoy.TargetAndBuoyAngle))<0.1)