import unittest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ''))
from api import *
from simulator import *

class testApi(unittest.TestCase):
    def setUp(self):
      self.ApiControl = ApiControl(Simulator())
      
    def testGetData(self):
      self.assertTrue(self.ApiControl.getOverviewData(), "no data")
    def testGetDebug(self):
      self.assertTrue(self.interface.getDebugMessages(), "no debug data")
        
if __name__ == '__main__':
    unittest.main()