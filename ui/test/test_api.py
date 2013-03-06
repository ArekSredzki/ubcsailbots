import unittest
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ''))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '../control/'))
print sys.path
from api import *
from simulator import *

class testApi(unittest.TestCase):
    def setUp(self):
      self.ApiControl = ApiControl(Simulator())
      
    def testGetData(self):
      self.assertTrue(self.ApiControl.getOverviewData(), "no data")
#    def testGetDebug(self):
#      self.assertTrue(self.ApiControl.getDebug(), "no debug data")
      
    def testSetInstruction(self):
      jsondata= '{"challenge":"NONE","waypoints":[[49.274801413633796,-123.18957755573376,"pointToPoint"]],"boundaries":[[49.274801907844804,-123.18956964070462,50]]}'
      controlInstructions = self.ApiControl.initControlInstructionsObject(json.loads(jsondata))
      self.assertEqual(controlInstructions.challenge, "NONE")
      self.assertEqual(controlInstructions.waypoints[0].coordinate.lat, 49.274801413633796)
      self.assertEqual(controlInstructions.waypoints[0].coordinate.long, -123.18957755573376)
      self.assertEqual(controlInstructions.waypoints[0].wtype, "pointToPoint")
      self.assertEqual(controlInstructions.boundaries[0].coordinate.lat, 49.274801907844804)
      self.assertEqual(controlInstructions.boundaries[0].coordinate.long, -123.18956964070462)
      self.assertEqual(controlInstructions.boundaries[0].radius, 50)
      

if __name__ == '__main__':
    unittest.main()