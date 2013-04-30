# Unit tests for the guihandler
import sys, os
sys.path.append(os.path.abspath('../'))
import unittest
from control import gui_handler
from control import global_vars as gVars
from control import static_vars as sVars
from control.datatype import datatypes
from datetime import datetime
class TestGuiHandler(unittest.TestCase):
    def setUp(self):
        self.gui_handler = gui_handler.GuiHandler()
        gVars.taskStartTime = datetime.now()
    
    def resetGlobVar(self):
        gVars.boundaries = []
        gVars.currentData = datatypes.ArduinoData()
        gVars.functionQueue = []  
        gVars.instructions = None
        gVars.queueParameters = []
          
    def testSetInstructionsWithNoChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.NO_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.gui_handler.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.GO_TO])
        self.assertEqual(gVars.queueParameters, [(datatypes.GPSCoordinate(1, 1), )])
    
    def testSetInstructionsWithNavChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.NAVIGATION_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.gui_handler.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.NAVIGATION_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
    
    def testSetInstructionsWithStationKeepChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.STATION_KEEPING_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.gui_handler.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.STATION_KEEPING_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
    
    def testSetInstructionsWithLDChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.LONG_DISTANCE_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.gui_handler.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.LONG_DISTANCE_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
         
    def testGetCurrentData(self):
        self.resetGlobVar()
        self.currdata = datatypes.ArduinoData(0, 1, 2, 3, datatypes.GPSCoordinate(4, 4) , 5, 6, 7, 0, 20)
        gVars.currentData = self.currdata
        self.gui_handler.getData()
        if (not gVars.taskStartTime):
            seconds = None
        else:
            seconds = (datetime.now() - gVars.taskStartTime).total_seconds()
            seconds = round(seconds)
        self.assertEqual(self.gui_handler.getData(), {"telemetry":{"Heading": self.currdata.hog, "COG" : self.currdata.cog, "SOG" : self.currdata.sog, "AWA" : self.currdata.awa, "latitude": self.currdata.gps_coord.lat , "longitude" : self.currdata.gps_coord.long, "SheetPercent": self.currdata.sheet_percent, "Rudder":self.currdata.rudder},
                  "connectionStatus":{"gpsSat":self.currdata.num_sat,"HDOP":self.currdata.gps_accuracy, "automode":self.currdata.auto},
                  "currentProcess":{"name":gVars.currentProcess,"Starttime":seconds}})
        
if __name__ == '__main__':
    unittest.main()
