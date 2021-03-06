# Create simulation data
import json
import unittest
import math
from random import *


def navigationChallenge(arg):
    pass

# Run Station Keeping challenge
# arg must be a tuple in format:
#    TODO
def stationKeepingChallenge(arg):
    pass

# Run Long Distance challenge
# arg must be a tuple in format:
#    TODO
def longDistanceChallenge(arg):
    pass

# Run Point to Point logic
# arg must be a tuple in format:
#    TODO
def pointToPoint(arg):
    pass

# Run Station Keep logic
# arg must be a tuple in format:
#    TODO
def stationKeep(arg):
    pass

# Run Round Buoy logic
# arg must be a tuple in format:
#    TODO
def roundBuoy(arg):
    pass

def setBoundary(coordinate, radius):
    #Boundary format: [<GPSCoordinate>, <radius(float)>]
    pass





class Simulator:
    def __init__(self):
        # Declare all public instance variables
        seed() 
        self.latitude = 49.27480
        self.longitude = -123.18960
        # sailSheet is updated when the wind changes direction
        self.sailSheet = 50
        self.update()
        
    def update(self):
        self.onlineOffline = self.genYesNo(99)
        self.batteryLevel = self.genBatteryLevel()
        self.gpsSatelliteNumber = self.genGpsSatelliteNumber()
        self.gpsAccuracy = self.genGpsAccuracy()
        self.speedOverGround = self.genSpeedOverGround()
        # updating the wind direction also updates the sail sheet
        self.windDirection = self.genWindDirection()
        self.timeRemaining = self.genTimeRemaining()
        self.latitude += 0.00001
        self.longitude += 0.00001
        self.boatHeading = self.genBoatHeading()
    def init(self):
        self.onlineOffline = genYesNo(99)
        self.batteryLevel = genBatteryLevel()
        
    def probChange(self, probability):
        # Takes a percentage of probability change
        i = randint(0,100)
        if i < probability:
            return True
        else:
            return False
    
    def genYesNo(self, probabilityOfYes=50):
        if randint(0,100) <= probabilityOfYes:
            return "yes";
        else:
            return "no";
    
    def genBoatHeading(self):
        try:
            self.boatHeading
        except AttributeError:
            # Not defined, generate an initial value
            return randint(0,360)
        else:
            # Variable is defined
            if self.probChange(80):
                if randint(0,1) == 1:
                    return self.boatHeading + randint(0,10)
                else:
                    return self.boatHeading - randint(0,10)
            else:
                return self.boatHeading
    
    
    def genBatteryLevel(self):
        try:
            self.batteryLevel
        except AttributeError:
            # Not defined, generate an initial value
            i = randint(0,2)
            if i == 0:
                return "empty"
            elif i == 1:
                return "partial"
            else:
                return "full"
        else:
            # Variable is defined
            if self.probChange(10):
                if self.batteryLevel == "empty" or self.batteryLevel == "full":
                    return "partial"
                else:
                    if randint(0,1) == 1:
                        return "full"
                    else:
                        return "empty"
            else:
                return self.batteryLevel
                
    def genWindDirection(self):
        # this function also has to update the sailSheet, which changes according to wind
        try:
            self.windDirection
        except AttributeError:
            # Not defined, generate an initial value
            return randint(0,360)
        else:
            # Variable is defined
            if self.probChange(80):
                if randint(0,1) == 1 or (self.sailSheet < 0 and self.sailSheet < 100):
                    self.sailSheet = self.sailSheet + randint(0,10)
                    return self.windDirection + randint(0,10)
                else:
                    self.sailSheet = self.sailSheet - randint(0,10)
                    return self.windDirection - randint(0,10)
            else:
                return self.windDirection
        
    def genTimeRemaining(self):
        try:
            self.timeRemaining
        except AttributeError:
            # Not defined, generate an initial value
            return randint(0,10*60)
        else:
            # Variable is defined
            if self.timeRemaining <= 0:
                return randint(0,10*60)
            elif self.probChange(1):
                return self.timeRemaining + randint(0,5)
            else:
                return self.windDirection - randint(1,4)
    
    def genGpsSatelliteNumber(self):
        try:
            self.gpsSatelliteNumber
        except AttributeError:
            # Variable is not defined
            return randint(0,24)
        else:
            # Variable is defined
            if self.probChange(20):
                return randint(0,24)
            else:
                return self.gpsSatelliteNumber
    
    def genGpsAccuracy(self):
        # Generate random number for GPS Accuracy. This number should be more likely to be a high value (up to 4)
        # Weuse a cosine function in order to "weight" the randomness towards high values
        return math.floor(math.cos(random())*4)
    
        
    def genSpeedOverGround(self):
        try:
            self.speedOverGround
        except AttributeError:
            # Not defined, generate an initial value
            return randint(0,4)
        else:
            # Variable is defined
            if random() == 1 or self.speedOverGround < 1:
                return self.speedOverGround + 1
            else:
                return self.speedOverGround - 1
    
    
    
    def getData(self):
        self.update()
        overviewData =  {"connectionStatus": {"onlineOffline": self.onlineOffline, "batteryLevel": self.batteryLevel, "gpsSatelliteNumber": self.gpsSatelliteNumber, "gpsAccuracy": self.gpsAccuracy, "hardwareHealth": "good"},
                        "telemetry": {"speedOverGround": self.speedOverGround, "windDirection": self.windDirection, "currentManeuver": "tracking", "latitude": self.latitude, "longitude": self.longitude, "sailSheet": self.sailSheet, "boatHeading": self.boatHeading},
                        "currentProcess": {"task": "Keep Away", "timeRemaining": self.timeRemaining, "timeToCompletion": 12},                                                  
                        }
        return overviewData
    
    def getOverviewDataAsJson(self):
        return json.dumps(self.getData())
    
    def getInstructions(self):
        self.update()
        instructionData = {"challenge": {"currentlyRunning": "Point-to-Point"},
                           "waypoints": {"indicator": "123"},
                           "boundaries": {"indicator":[2,3,4]},
                           }
        return instructionData
    
    def getInstructionsDataAsJson(self):
        return json.dumps(self.getInstructions())
        
    
    # forces data to be updated from the Control Unit
    def forceDataUpdate(self):
        pass

        
    