import sys
sys.path.append('..')
import unittest
from control import global_vars as gVars
print sys.path
from control.logic import roundbuoy
from control import sailbot_logger
from control.datatype import datatypes

class TestRoundBuoy(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.round_buoy = roundbuoy.RoundBuoy()
        
        
    def testFindRightBuoyPoint(self):
        gVars.currentData.gps_coord.lat = 0
        gVars.currentData.gps_coord.long = 0
        
        return