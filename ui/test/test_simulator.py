import unittest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ''))
from simulator import *

class testSimulator(unittest.TestCase):
    def setUp(self):
      self.interface = Simulator()
    def testGetData(self):
      self.assertTrue(self.interface.getData(), "no data")
    def testUpdate(self):
      oldData = self.interface.getData()
      newData = self.interface.getData()
      self.assertNotEqual(oldData,newData, "data hasn't changed after update")

        
if __name__ == '__main__':
    unittest.main()