#Unit tests of standardcalc.py module
import sys, os
sys.path.append(os.path.abspath('../../'))
import unittest
from control import GlobalVars
print sys.path
from control.logic import pointtopoint
from control import sailbotlogger
import control.datatype.datatypes as datatypes

class TestPointToPoint(unittest.TestCase):
  def setUp(self):
    GlobalVars.logger = sailbotlogger.logger()
    self.p2p = pointtopoint.PointToPoint()
      
  def testWhichTackWanted(self):
    initialTack=None
    self.p2p.AWA = 30
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))
    self.assertTrue(self.p2p.portTackWanted(initialTack))

    self.p2p.AWA = -30
    self.assertTrue(self.p2p.starboardTackWanted(initialTack))
    self.assertFalse(self.p2p.portTackWanted(initialTack))

    self.p2p.AWA = -150
    self.assertTrue(self.p2p.starboardTackWanted(initialTack))
    self.assertFalse(self.p2p.portTackWanted(initialTack))

    self.p2p.AWA = 150
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))
    self.assertTrue(self.p2p.portTackWanted(initialTack))

    self.p2p.AWA = 0
    self.assertFalse(self.p2p.starboardTackWanted(initialTack))
    self.assertTrue(self.p2p.portTackWanted(initialTack))

  def testdoWeStillWantToTack(self):
    self.p2p.GPSCoord = datatypes.GPSCoordinate(49,-123)
    self.p2p.Dest = datatypes.GPSCoordinate(49.1,-123) # 0 degrees, N
    
    self.p2p.hog = 0 # N
    self.assertTrue(self.p2p.doWeStillWantToTack())
    
    self.p2p.hog = 45 # NE
    self.assertTrue(self.p2p.doWeStillWantToTack())
    
    self.p2p.hog = 90 # E
    self.assertFalse(self.p2p.doWeStillWantToTack())
    
    self.p2p.hog = -45 # NW
    self.assertTrue(self.p2p.doWeStillWantToTack())
    
    self.p2p.hog = -90 # NW
    self.assertFalse(self.p2p.doWeStillWantToTack())
    