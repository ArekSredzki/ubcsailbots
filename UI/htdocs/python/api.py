import json


""" Handles all data that is passed from the API 
*EDITING NOTE: Please make sure you understand how python handles classes before making any edits to this file. Mutable data types in 
        python have to be declared as instance variables and NOT as public variables in global scope. Global scope variables are shared
        between instances and will cause messy results that do not report any errors. 
"""
class ApiControl:
    def __init__(self):
        # Declare all public instance variables
        self.hardwareData = ""
        
    def getOverviewData(self):
        overviewData =  {"connectionStatus": {"onlineOffline": "yes", "batteryLevel": "full", "gpsNumberOfSatellites": 12, "gpsAccuracy": 2, "hardWareHealth": "good"},
                        "telemetry": {"speedOverGround": 14, "windDirection": 10, "currentManeuver": "tracking"},
                        "currentProcess": {"task": "Keep Away", "timeRemaining": 1400, "timeToCompletion": 12},                           
                        }
        return overviewData
    
    def getOverviewDataAsJson(self):
        return json.dumps(self.getOverviewData())
    
    def getInstructionsData(self):
        instructionData = {"challenge": {"currentlyRunning": "Point-to-Point"},
                           "waypoints": {"indicator": "123"},
                           "boundaries": {"indicator":[2,3,4]},
                           }
        return instructionData
    
    def getInstructionsDataAsJson(self):
        return json.dumps(self.getInstructionsData())
        
    
    # forces data to be updated from the Control Unit
    def forceDataUpdate(self):
        pass

        
    