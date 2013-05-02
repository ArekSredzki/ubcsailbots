'''
Created on Feb 2, 2013

Mock Arduino which should simulate changing wind conditions and return simulated
boat data that can be used by the control logic and gui.
-   By creating a mock arduino object, you may call functions which will return mock
    data.  All of the data will be simulated to show relative wind conditions and
    will be reactive upon functions called to the Arduino
    
@author: joshandrews
'''

from control.datatype import datatypes
from control.logic import standardcalc
import random
import math
import time

EARTH_RADIUS = 6378140

# Parameters which may be changed to affect how the simulation runs
ALLOW_WIND_REVERSAL = False
STRONG_CURRENT = False

# Set this to hold a constant AWA.  Otherwise set it to None.  Useful 
# for functionality testing on Challenges. Not as much useful point to point.
STATIC_AWA = 0

class arduino:
    def __init__(self):
        
        # Sets initial vectors and magnitudes for wind and boat
        self.flipflag = False
        self.windStrength = round(random.uniform(1, 5), 0)
        self.actualWindAngle = round(random.uniform(-179, 180), 2)
        self.actualWindSpeed = round(random.uniform(3, 6), 2)*self.windStrength
        self.idealBoatSpd = round(random.uniform(.5, 1), 2)*self.windStrength
        self.previousx = None
        self.steerByApparentWind = False
        self.steerByApparentWindAngle = 0
        if (STRONG_CURRENT):
            self.currplusmin = round(random.uniform(-4, -2), 2)
        else:
            self.currplusmin = 0
        
        print("Current Plus/Min: " + str(self.currplusmin))  
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.arduinoData = datatypes.ArduinoData(hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatypes.GPSCoordinate(49.27480, -123.18960), 0, 
                          15, 80, 1, 20)
        print(self.arduinoData)
        
    def getFromArduino(self):
        self._updateAll()
        return self.arduinoData
    
    def tack(self, weather, tack):
        hog = self.arduinoData.hog
       
        # Format
        #     Tack: Port=0 Stbd=1
        if (tack == 1):
            hog += 100
        else:
            hog -= 100
            
        hog = standardcalc.boundTo180(hog)
        
        self.arduinoData.hog = hog
    
    def gybe(self, x):
        tempspeed = self.arduinoData.sog
        self.arduinoData.sog = 0
        self.arduinoData.hog = standardcalc.boundTo180(self.arduinoData.hog+180)
        time.sleep(4)
        self.arduinoData.sog = tempspeed
    
    def adjust_sheets(self, sheet_percent):                                                
        self.arduinoData.sheet_percent = sheet_percent
        
    def steer(self, method, degree):
        if method == 2:
            self.arduinoData.hog = self.arduinoData.awa + degree
            self.steerByApparentWind = True
            self.steerByApparentWindAngle = degree
        else:
            self.arduinoData.hog = degree
            self.steerByApparentWind = False
    
    def _updateActualWind(self):
        # Updates actual wind angle
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += random.uniform(-.2, 0)
        else:
            self.actualWindAngle += random.uniform(-.1, .1)     
        self.actualWindAngle = standardcalc.boundTo180(self.actualWindAngle)  
        
    def _updateHOG(self):
        # Updates slight variation in HOG      
        self.arduinoData.hog += (round(random.uniform(-.1, .1), 2) + self.currplusmin)
        if self.steerByApparentWind:
            self.arduinoData.hog = self.arduinoData.awa + self.steerByApparentWindAngle
    
    def _updateCOG(self):
        # Sets the course over ground
        if (math.fabs(self.arduinoData.cog + self.currplusmin - self.arduinoData.hog) < .4):
            self.arduinoData.cog += round(random.uniform(-.1, .1), 2)
        elif (self.arduinoData.cog + self.currplusmin < self.arduinoData.hog):
            self.arduinoData.cog += round(random.uniform(0, 5), 2)
        elif (self.arduinoData.cog + self.currplusmin > self.arduinoData.hog):
            self.arduinoData.cog += round(random.uniform(-5, 0), 2)
        self.arduinoData.cog = standardcalc.boundTo180(self.arduinoData.cog)
    
    def _updateSOG(self):
        # Gets the boat up to speed and allows for a little variation
        if (math.fabs(self.arduinoData.sog - self.idealBoatSpd) < .2):
            self.arduinoData.sog += round(random.uniform(-.1, .1), 2)
        elif (self.arduinoData.sog < self.idealBoatSpd):
            self.arduinoData.sog += round(random.uniform(0, .2), 2)
        elif (self.arduinoData.sog >= self.idealBoatSpd):
            self.arduinoData.sog += round(random.uniform(-.2, 0), 2)
    
    def _updateAWA(self):
        if STATIC_AWA == None:
            # Sets the apparent wind angle
            boat_bearing = self.arduinoData.hog
            
            # Reverse direction for boat vector
            if (boat_bearing >= 0):
                boat_bearing -= 180
            else:
                boat_bearing += 180
            boat_speed = self.arduinoData.sog
            
            # Reverse direction for wind vector
            wind_bearing = self.actualWindAngle
            if (wind_bearing >= 0):
                wind_bearing -= 180
            else:
                wind_bearing += 180
                
            wind_speed = self.actualWindSpeed
            
            boat_x = boat_speed * math.cos(boat_bearing)
            boat_y = boat_speed * math.sin(boat_bearing)
            wind_x = wind_speed * math.cos(wind_bearing)
            wind_y = wind_speed * math.sin(wind_bearing)
            
            x = boat_x + wind_x
            y = boat_y + wind_y
            
            if self.previousx is None:
                self.previousx = x
            
            awa = math.atan(y/x)
    
            if(math.copysign(self.previousx, x) != self.previousx or self.flipflag): 
                if (not self.flipflag):
                    self.flipflag = True
                elif (math.copysign(self.previousx, x) != self.previousx):
                    self.flipflag = False
                    
                print(str(self.previousx) + ", " + str(x))  
                if(awa > 0):
                    awa -= math.pi
                else:
                    awa += math.pi
             
            awa = math.degrees(awa)
                
            awa -= self.arduinoData.hog
            
            awa = standardcalc.boundTo180(awa)
            
            self.previousx = x
        else:
            awa = standardcalc.boundTo180(standardcalc.boundTo360(STATIC_AWA)-standardcalc.boundTo180(self.arduinoData.hog))
        
        self.arduinoData.awa = standardcalc.boundTo180(awa)
    
    def _updateGPS(self):
        # Calculation for change in GPS Coordinate
        heading = self.arduinoData.hog
        
        # Convert to 360 degree heading
        if (heading < 0):
            heading = 360 + heading
        
        lon0 = self.arduinoData.gps_coord.long
        lat0 = self.arduinoData.gps_coord.lat
        heading = self.arduinoData.hog
        speed = self.arduinoData.sog
        
        x = speed * math.sin(heading*math.pi/180)
        y = speed * math.cos(heading*math.pi/180)
        
        lat = lat0 + 180 / math.pi * y / EARTH_RADIUS;
        lon = lon0 + 180 / math.pi / math.sin(lat0*math.pi/180) * x / EARTH_RADIUS;
        
        self.arduinoData.gps_coord.lat = lat
        self.arduinoData.gps_coord.long = lon
    
    def _updateAll(self):
        self._updateActualWind()    
        self._updateHOG()
        self._updateCOG()
        self._updateAWA()
        self._updateSOG()
        self._updateGPS()     
        