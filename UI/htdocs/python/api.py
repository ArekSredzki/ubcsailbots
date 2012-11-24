import json


""" Handles all data that is passed from the API 
*EDITING NOTE: Please make sure you understand how python handles classes before making any edits to this file. Mutable data types in 
        python have to be declared as instance variables and NOT as public variables in global scope. Global scope variables are shared
        between instances and will cause messy results that do not report any errors. 
"""
class ApiControl:
    def __init__(self):
        # Declare all public instance variables
        self.hardwareData = "test"
        
    def getOverviewData(self):
        overviewData =  {"connectionStatus": {"onlineOffline": "yes", "batteryLevel": "full", },
                        "telemetry": {"speedOverGround": "14", "windDirection": "10", "currentManeuver": "tracking"},
                        "currentProcess": {"task": "Keep Away", "timeRemaining": "1400", "timeToCompletion": "12222"},                           
                        }
        return overviewData
    
    def getOverviewDataAsJson(self):
        return json.dumps(self.getOverviewData())
    
    # forces data to be updated from the Control Unit
    def forceDataUpdate(self):
        pass
    
    # Formats all the instance data for the <head> block as valid HTML in the 'headBlock' variable.
    def format(self):
        self.cssHeadStyles = '\n'.join(self.cssHeadStyles) + '\n'
        # Include widgets last to ensure that all the jQuery files are already loaded
        for widget in self.widgets[:]:
            self.jsIncludes += '<script src ="static/js/widgets/' + widget + '.js"></script>\n'
            self.cssIncludes += '<link rel="styesheet" type="text/css" href="static/css/widgets/' + widget + '.css" />\n' 
        # Create headBlock 
        self.headBlock = '<title>' + self.title + '</title>\n' + '\n' + self.jsIncludes + '\n' + self.cssIncludes + '\n' + self.jsHeadFunctions + '\n' + self.cssHeadStyles
        

        
    