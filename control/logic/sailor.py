from control.parser import parsing
from control.logic import standardcalc
from control import global_vars as gVars
from os import path

class Sailor:
    #constants
    COMPASS_METHOD = 0
    COG_METHOD = 1
    AWA_METHOD = 2
    TACKING_ANGLE = 30

    def __init__(self):
        self.sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))            

    def adjustSheetsAndSteerByCompass(self, AWA, heading):
        gVars.arduino.adjust_sheets(self.sheetList[abs(int(AWA))][gVars.currentColumn])
        gVars.arduino.steer(self.COMPASS_METHOD,heading)  
            
    def adjustSheetsAndSteerByApparentWind(self, tackAngleMultiplier, AWA):
        gVars.arduino.adjust_sheets(self.sheetList[abs(int(AWA))][gVars.currentColumn])
        gVars.arduino.steer(self.AWA_METHOD,tackAngleMultiplier*self.TACKING_ANGLE)
        