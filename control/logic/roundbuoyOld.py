'''
Created on Apr 14, 2013

@author: joshandrews
'''

import math
from control.logic import standardcalc
from control.logic import pointtopoint
from control import global_vars as gVars
from control.datatype import datatypes
from control import sailing_task

class RoundBuoy(sailing_task.SailingTask):
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint
        
    def run(self, BuoyLoc, FinalLoc=None, port=True):
        GPSCoord = gVars.currentData.gps_coord
        if FinalLoc == None:
            FinalLoc = GPSCoord
        ANGLE_BOAT_TO_TARGET_WRT_BUOY = 138
        calc = self.roundBuoyCalc(BuoyLoc, ANGLE_BOAT_TO_TARGET_WRT_BUOY, 10)
        
        X = calc[0]
        Dest = calc[1] # Meters, Distance from boat to target (after buoy)
        angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
        move = None
        
        if port:
            move = self.portCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X)
        else:
            move = self.starCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X)
                    
        # move = [long, lat, long, lat]
        moveLong = move[0]
        moveLat = move[1]
        moveLong2 = move[2]
        moveLat2 = move[3]
        
        
        moveLong *= Dest 
        moveLat *= Dest 
        destination = standardcalc.GPSDistAway(GPSCoord, moveLong, moveLat)
    
        if (GPSCoord.long >= standardcalc.GPSDistAway(destination, 10, 0).long): 
            gVars.logger.info("Going to first point")
            self.pointtopoint.run(datatypes.GPSCoordinate(destination.lat, destination.long),1)
            
            
        # Checks if the boat needs to round the buoy or just pass it
        angleToTarget = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, FinalLoc)
        angleToBuoy = standardcalc.angleBetweenTwoCoords(gVars.currentData.gps_coord, BuoyLoc)
        
        if angleToTarget < standardcalc.boundTo180(angleToBuoy + 15) and angleToTarget > standardcalc.boundTo180(angleToBuoy - 15): 
            destination = standardcalc.GPSDistAway(GPSCoord, moveLong2, moveLat2)
            self.pointtopoint.run(datatypes.GPSCoordinate(destination.lat, destination.long),1)
            
        return 0
    
    def portCalcRoundBuoy(self, GPSCoord, BuoyLoc, angleToNorth, X):
        if GPSCoord.long > BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
            # 1st Point: Quadrant 3
            moveLong = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
            moveLat = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
            # 2nd Point: Quadrant 4
            moveLong2 = abs(math.sin(angleToNorth -90 - X)) # + X Movement
            moveLat2 = abs(math.cos(angleToNorth - 90 - X)) * -1 # - Y Movement
        elif GPSCoord.long < BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
            # 1st Point: Quadrant 4
            moveLong = abs(math.cos(angleToNorth -90 - X)) # + X Movement
            moveLat = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
            # 2nd Point: Quadrant 1
            moveLong2 = abs(math.cos(angleToNorth - X)) # + X Movement
            moveLat2 = abs(math.sin(angleToNorth - X)) # + Y Movement
        elif GPSCoord.long < BuoyLoc.long and GPSCoord.lat < BuoyLoc.lat:
            # 1st Point: Quadrant 1
            moveLong = abs(math.sin(angleToNorth - X)) # + X Movement
            moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement
            # 2nd Point: Quadrant 2
            moveLong2 = abs(math.sin(angleToNorth - X)) * - 1 # - X Movement
            moveLat2 = abs(math.cos(angleToNorth - X)) # + Y Movement 
        else:
            # 1st Point: Quadrant 2
            moveLong = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
            moveLat = abs(math.cos(angleToNorth + X)) # + Y Movement 
            # 2nd Point: Quadrant 3
            moveLong2 = abs(math.cos(180 - angleToNorth + X)) * -1 # - X movement 
            moveLat2 = abs(math.sin(180 - angleToNorth + X)) * - 1 # - Y movement
        
        move = [moveLong, moveLat, moveLong2, moveLat2]
        
        return move
    
    def starCalcRoundBuoy(self, GPSCoord, BuoyLoc, angleToNorth, X):
        if GPSCoord.long > BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
            # 1st Point: Quadrant 3
            moveLong = abs(math.cos(180 - angleToNorth + X)) * -1 # - X movement 
            moveLat = abs(math.sin(180 - angleToNorth + X)) * - 1 # - Y movement
            # 2nd Point: Quadrant 2
            moveLong2 = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
            moveLat2 = abs(math.cos(angleToNorth + X)) # + Y Movement 
        elif GPSCoord.long < BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
            # 1st Point: Quadrant 4
            moveLong = abs(math.sin(angleToNorth -90 - X)) # + X Movement
            moveLat = abs(math.cos(angleToNorth - 90 - X)) * -1 # - Y Movement
            # 2nd Point: Quadrant 3
            moveLong2 = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
            moveLat2 = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
        elif GPSCoord.long < BuoyLoc.long and GPSCoord.lat < BuoyLoc.lat:
            # 1st Point: Quadrant 1
            moveLong = abs(math.cos(angleToNorth - X)) # + X Movement
            moveLat = abs(math.sin(angleToNorth - X)) # + Y Movement
            # 2nd Point: Quadrant 4
            moveLong2 = abs(math.cos(angleToNorth -90 - X)) # + X Movement
            moveLat2 = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
        else:
            # 1st Point: Quadrant 2
            moveLong = abs(math.sin(angleToNorth - X)) * - 1 # - X Movement
            moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement 
            # 2nd Point: Quadrant 1
            moveLong2 = abs(math.sin(angleToNorth - X)) # + X Movement
            moveLat2 = abs(math.cos(angleToNorth - X)) # + Y Movement
            
        move = [moveLong, moveLat, moveLong2, moveLat2]
        
        return move
    
    def roundBuoyCalc(self, BuoyLoc, gamma, DisTargetToBuoy=10):
        GPSCoord = gVars.currentData.gps_coord
        
        DisBoatToBuoy = standardcalc.distBetweenTwoCoords(BuoyLoc, GPSCoord)
        Dest = math.sqrt(DisTargetToBuoy**2 + DisBoatToBuoy**2 - 2*DisTargetToBuoy*DisBoatToBuoy*math.cos(math.radians(gamma)))
        theta2 = math.radians(180 - gamma)
        gVars.logger.info("theta2: " + str(theta2))
        gVars.logger.info("cos(theta2): " + str(math.cos(theta2)))
        x1 = math.cos(theta2)*DisTargetToBuoy
        gVars.logger.info(" distboattobuoy: " +str(DisBoatToBuoy) + " x1: "+str(x1) + " dest: "+ str(Dest))
        outX = math.acos((DisBoatToBuoy + x1)/Dest)
        
        calc = [outX, Dest]
        
        return calc