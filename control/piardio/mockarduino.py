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
import control.StaticVars as sVars
import random
import math
import thread

EARTH_RADIUS = 6378140

# Parameters which may be changed to affect how the simulation runs
ALLOW_WIND_REVERSAL = False
STRONG_CURRENT = False

# Set this to hold a constant AWA.  Otherwise set it to None.  Useful 
# for functionality testing on Challenges. Not as much useful point to point.
STATIC_AWA = 45

class arduino:
    def __init__(self):
        
        # Sets initial vectors and magnitudes for wind and boat
        self.flipflag = False
        self.windStrength = round(random.uniform(1, 5), 0)
        self.actualWindAngle = round(random.uniform(-179, 180), 2)
        self.actualWindSpeed = round(random.uniform(3, 6), 2)*self.windStrength
        self.idealBoatSpd = round(random.uniform(.5, 1), 2)*self.windStrength
        self.previousx = None
        if (STRONG_CURRENT):
            self.currplusmin = round(random.uniform(-4, 4), 2)
        else:
            self.currplusmin = round(random.uniform(-1, 1), 2)
        
        print("Current Plus/Min: " + str(self.currplusmin))  
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.ardArray = [hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatypes.GPSCoordinate(49.27480, -123.18960), 0, 
                          15, 80, 1, 20]
        print(self.ardArray)
        
    def getFromArduino(self):
        self._updateAll()
        return self.ardArray
    
    def tack(self, weather, tack):
        hog = self.ardArray[sVars.HOG_INDEX]
       
        # Format
        #     Tack: Port=0 Stbd=1
        if (tack == 1):
            hog += 100
        else:
            hog -= 100
            
        hog = standardcalc.boundTo180(hog)
        
        self.ardArray[sVars.HOG_INDEX] = hog
    
    def gybe(self, x):
        pass
    
    def adjust_sheets(self, sheet_percent):                                                
        self.ardArray[sVars.SHT_INDEX] = sheet_percent
        
    def steer(self, method, degree):
        self.ardArray[sVars.HOG_INDEX] = degree
    
    def _updateActualWind(self):
        # Updates actual wind angle
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += random.uniform(-.2, 0)
        else:
            self.actualWindAngle += random.uniform(-.1, .1)     
        self.actualWindAngle = standardcalc.boundTo180(self.actualWindAngle)  
        
    def _updateHOG(self):
        # Updates slight variation in HOG      
        self.ardArray[sVars.HOG_INDEX] += round(random.uniform(-.1, .1), 2)
    
    def _updateCOG(self):
        # Sets the course over ground
        if (math.fabs(self.ardArray[sVars.COG_INDEX]+self.currplusmin-self.ardArray[sVars.HOG_INDEX]) < .4):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sVars.COG_INDEX]+self.currplusmin < self.ardArray[sVars.HOG_INDEX]):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(0, 5), 2)
        elif (self.ardArray[sVars.COG_INDEX]+self.currplusmin > self.ardArray[sVars.HOG_INDEX]):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(-5, 0), 2)
        self.ardArray[sVars.COG_INDEX] = standardcalc.boundTo180(self.ardArray[sVars.COG_INDEX])
    
    def _updateSOG(self):
        # Gets the boat up to speed and allows for a little variation
        if (math.fabs(self.ardArray[sVars.SOG_INDEX]-self.idealBoatSpd) < .2):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sVars.SOG_INDEX] < self.idealBoatSpd):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(0, .2), 2)
        elif (self.ardArray[sVars.SOG_INDEX] >= self.idealBoatSpd):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(-.2, 0), 2)
    
    def _updateAWA(self):
        if STATIC_AWA == None:
            # Sets the apparent wind angle
            boat_bearing = self.ardArray[sVars.HOG_INDEX]
            
            # Reverse direction for boat vector
            if (boat_bearing >= 0):
                boat_bearing -= 180
            else:
                boat_bearing += 180
            boat_speed = self.ardArray[sVars.SOG_INDEX]
            
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
                
            awa -= self.ardArray[sVars.HOG_INDEX]
            
            awa = standardcalc.boundTo180(awa)
            
            self.previousx = x
        else:
            awa = STATIC_AWA
        
        self.ardArray[sVars.AWA_INDEX] = awa
    
    def _updateGPS(self):
        # Calculation for change in GPS Coordinate
        heading = self.ardArray[sVars.HOG_INDEX]
        
        # Convert to 360 degree heading
        if (heading < 0):
            heading = 360 + heading
        
        lon0 = self.ardArray[sVars.GPS_INDEX].long
        lat0 = self.ardArray[sVars.GPS_INDEX].lat
        heading = self.ardArray[sVars.HOG_INDEX]
        speed = self.ardArray[sVars.SOG_INDEX]
        
        x = speed * math.sin(heading*math.pi/180)
        y = speed * math.cos(heading*math.pi/180)
        
        lat = lat0 + 180 / math.pi * y / EARTH_RADIUS;
        lon = lon0 + 180 / math.pi / math.sin(lat0*math.pi/180) * x / EARTH_RADIUS;
        
        self.ardArray[sVars.GPS_INDEX].lat = lat
        self.ardArray[sVars.GPS_INDEX].long = lon
    
    def _updateAll(self):
        self._updateActualWind()    
        self._updateHOG()
        self._updateCOG()
        self._updateSOG()
        self._updateAWA()
        self._updateGPS()     
        