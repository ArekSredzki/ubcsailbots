'''
Created on Jan 21, 2013

GUI Handler for the control logic
-   The GUI sends instructions to the GUIHandler which 
    will parse the data and add function queues.

@author: joshandrews
'''

import control.GlobalVars as gVars
import control.StaticVars as sVars
import control.challenge as challenge
from datetime import timedelta
from datetime import datetime

# GUI Handler Class
#    * GUI can call any of these functions and rest will be taken care of
class GuiHandler:
    
    # when the user sends new instructions
    # the control code will update its instructions object
    # When the remote control signals a switch to auto then the instructions are carried out
    def setInstructions(self, instructionsData):
        # Stores current boundaries
        gVars.currentProcess = None
        gVars.boundaries = instructionsData.boundaries
        gVars.instructions = instructionsData
        # Stores function queue and parameter queue
        if (instructionsData.challenge == sVars.NO_CHALLENGE):
            for waypoint in instructionsData.waypoints:
                gVars.functionQueue.append(waypoint.wtype)
                gVars.queueParameters.append((waypoint.coordinate, ))
                
        else:
            gVars.functionQueue.append(instructionsData.challenge)
            gVars.queueParameters.append(tuple(instructionsData.waypoints))
            
        print gVars.currentProcess
    # returns the  instructions object
    def getInstructions(self):        #main.returninstructionsdataforgui
        return gVars.instructions
    
    # returns all the telemetry data as an object
    # ex. apparent wind, gps location, SOG, COG, heading, etc.
    def getData(self):
        currentData = gVars.currentData
        
        if (not gVars.taskStartTime):
            seconds = None
        else:
            seconds = (datetime.now() - gVars.taskStartTime).total_seconds()
            seconds = round(seconds)
            
        output = {"telemetry":{"Heading": currentData.hog, "COG" : currentData.cog, "SOG" : currentData.sog, "AWA" : currentData.awa, "latitude": currentData.gps_coord.lat , "longitude" : currentData.gps_coord.long, "SheetPercent": currentData.sheet_percent, "Rudder": currentData.rudder},
                  "connectionStatus":{"gpsSat":currentData.num_sat,"HDOP":currentData.gps_accuracy, "automode":currentData.auto}, 
                  "currentProcess":{"name":gVars.currentProcess, "Starttime":seconds}}
        return output
    
    #returns a string of debug messages
    def getDebugMessages(self):
        logger = gVars.logger
        buff = logger.buffer
        logger.clearBuffer()
        return buff
