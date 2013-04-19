#Unit tests of standardcalc.py module
import sys, os
sys.path.append(os.path.abspath('../../'))
import unittest
from control import GlobalVars
print sys.path
from control.logic import pointtopoint
from control import sailbotlogger

class TestPointToPoint(unittest.TestCase):
  def setUp(self):
    GlobalVars.logger = sailbotlogger.logger()
    self.p2p = pointtopoint.PointToPoint()
      
  def testStarboardTackWanted(self):
    initialTack=None
    self.p2p.AWA = 30
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))
    self.p2p.AWA = -30
    self.assertTrue(self.p2p.starboardTackWanted(initialTack))
    self.p2p.AWA = -150
    self.assertTrue(self.p2p.starboardTackWanted(initialTack))
    self.p2p.AWA = 150
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))
    self.p2p.AWA = 0
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))

  def testPortTackWanted(self):
    initialTack=None
    self.p2p.AWA = 30
    self.assertTrue(self.p2p.portTackWanted(initialTack))
    self.p2p.AWA = -30
    self.assertFalse(self.p2p.portTackWanted(initialTack))
    self.p2p.AWA = -150
    self.assertFalse(self.p2p.portTackWanted(initialTack))
    self.p2p.AWA = 150
    self.assertTrue(self.p2p.portTackWanted(initialTack))
    self.p2p.AWA = 0
    self.assertTrue(self.p2p.portTackWanted(initialTack))

  def testdoWeStillWantToTack(self):
    