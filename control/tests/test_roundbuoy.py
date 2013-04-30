import sys, os
sys.path.append(os.path.abspath('../../'))
import unittest
from control import global_vars as gVars
print sys.path
from control.logic import roundbuoy
from control import sailbot_logger
import control.datatype.datatypes as datatypes

class TestPointToPoint(unittest.TestCase):
    def setUp(self):
        gVars.logger = sailbot_logger.Logger()
        self.round_buoy = roundbuoy.RoundBuoy()
        
    def testFindFirstBuoyPoint(self):
        return