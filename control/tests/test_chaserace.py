import sys, os
sys.path.append(os.path.abspath('../../'))
import unittest
from control import global_vars as gVars
import control.datatype.datatypes as datatypes
from control.challenge import chaserace

class TestStartDirection(unittest.TestCase):
    def setUp(self):
        self.coords=[]
        self.coords.append(datatypes.GPSCoordinate(1.0,1.0))
        self.coords.append(datatypes.GPSCoordinate(1.0,2.0))
        self.coords.append(datatypes.GPSCoordinate(2.0,2.0))
        self.coords.append(datatypes.GPSCoordinate(2.0,1.0))
        self.chaseRace = chaserace.ChaseRace()
        gVars.instructions = datatypes.Instructions("none",[],[],"port",0)
        gVars.currentData = datatypes.ArduinoData(0, 1, 2, 3, datatypes.GPSCoordinate(4, 4) , 5, 6, 7, 0, 20)
    def testStarboardRounding(self):
        gVars.instructions.rounding = "starboard"
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(2.0,2.0)
        self.assertEquals(self.chaseRace.getStartDirection(self.coords),3)
    
    def testPortRounding(self):
        gVars.instructions.rounding = "port"
        gVars.currentData.gps_coord = datatypes.GPSCoordinate(2.0,2.0)
        self.assertEquals(self.chaseRace.getStartDirection(self.coords),1)      