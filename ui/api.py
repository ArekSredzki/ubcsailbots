import json
import control.datatype.datatypes as control
""" Handles all data that is passed from the API 
*EDITING NOTE: Please make sure you understand how python handles classes before making any edits to this file. Mutable data types in 
        python have to be declared as instance variables and NOT as public variables in global scope. Global scope variables are shared
        between instances and will cause messy results that do not report any errors. 
"""
class ApiControl:
    def __init__(self,interface):
        self.interface = interface
        # Declare all public instance variables
        self.hardwareData = ""
        # We need to update the interface with all current data. The interface class is static, but it may need to renew data

    def getOverviewData(self):
        overviewData = self.interface.getData()
        return overviewData
    
    def getOverviewDataAsJson(self):
        return json.dumps(self.getOverviewData())
    
    def getInstructionsDataAsJson(self):
        try:
            return self.jsonInstructionsData
        except:
          return "nodata"
        
    
    # forces data to be updated from the Control Unit
    def forceDataUpdate(self):
        pass
    
    def getDebug(self):
      pass
    
    def setInstructions(self,jsonData):
        self.jsonInstructionsData = jsonData
        instructions = json.loads(jsonData)        
        controlInstructions = self.initControlInstructionsObject(instructions)
        self.interface.setInstructions(controlInstructions)
        return 'basic setup successful!'
      
    def initControlInstructionsObject(self,instructions):
      waypointsList=[]
      boundariesList=[]
      for wpt in instructions['waypoints']:
        coordinate = control.GPSCoordinate(wpt[0],wpt[1])
        waypointsList.append(control.Waypoint(coordinate,wpt[2]))
      for bnd in instructions['boundaries']:
        coordinate = control.GPSCoordinate(bnd[0],bnd[1])
        boundariesList.append(control.Boundary(coordinate,bnd[2]))
      controlInstructions = control.Instructions(instructions['challenge'],waypointsList,boundariesList)
      return controlInstructions
