'''
Created on Jan 19, 2013

@author: joshandrews
'''
import time
import math
import sys
from os import path
from control.parser import parsing
from control.logic import standardcalc
from control import StaticVars as sVars
from control import GlobalVars as gVars
from control.datatype import datatypes
hog_index=sVars.HOG_INDEX
cog_index=sVars.COG_INDEX
sog_index=sVars.SOG_INDEX
awa_index=sVars.AWA_INDEX
gps_index=sVars.GPS_INDEX
sht_index=sVars.SHT_INDEX
aut_index=sVars.AUT_INDEX

COMPASS_METHOD = 0
COG_METHOD = 1
AWA_METHOD = 2

TACKING_ANGLE = 34 

end_flag=0

# --- Round Buoy Port---
# Input: Round Buoy location, Final bearing with respect to North
def roundBuoyPort(BuoyLoc, FinalBearing=None):
    roundBuoy(BuoyLoc)
    '''
    currentData = gVars.currentData
    
    if FinalBearing is None:
        FinalBearing = standardcalc.boundTo180(standardcalc.angleBetweenTwoCoords(currentData[gps_index], BuoyLoc)-179)
    
    GPSCoord = currentData[gps_index]
    # appWindAng = currentData[awa_index]
    InitCog = currentData[cog_index] # Course  over ground    
    InitHog = currentData[hog_index] # Heading over ground
    
    X = 16.64 # Degrees, Calculated
    Dest = 23.41 # Meters, Distance from boat to buoy
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    reflectLong = GPSCoord.long * -1 # Used for calculation ONLY, because longitude decreases from left to right
    quadDir = None
    
    if reflectLong > BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
        quadDir = 3;
        #For setting the 2nd point
        moveLong2 = abs(math.sin(angleToNorth -90 - X)) # + X Movement
        moveLat2 = abs(math.cos(angleToNorth - 90 - X)) * -1 # - Y Movement
    elif reflectLong < BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.cos(angleToNorth -90 - X)) # + X Movement
        moveLat = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
        quadDir = 4;
        #For setting the 2nd point
        moveLong2 = abs(math.cos(angleToNorth - X)) # + X Movement
        moveLat2 = abs(math.sin(angleToNorth - X)) # + Y Movement
    elif reflectLong < BuoyLoc.long and GPSCoord.lat < BuoyLoc.lat:
        moveLong = abs(math.sin(angleToNorth - X)) # + X Movement
        moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement
        quadDir = 1;
        moveLong2 = abs(math.sin(angleToNorth - X)) * - 1 # - X Movement
        moveLat2 = abs(math.cos(angleToNorth - X)) # + Y Movement 
    else:
        moveLong = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
        moveLat = abs(math.cos(angleToNorth + X)) # + Y Movement 
        quadDir = 2;
        moveLong2 = abs(math.cos(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat2 = abs(math.sin(180 - angleToNorth + X)) * - 1 # - Y movement
                
    moveLong *= Dest
    moveLat *= Dest 
    
    moveLong *= -1 # Convert back actual coordinates
    
    destination = standardcalc.GPSDistAway(GPSCoord, moveLong, moveLat)
    
    # 10 represents the degree of error around the destination point
    # Calls point to point function until it reaches location past buoy
    # Adding 10 does not increase the radius by 10 meters(ERROR!) - fixed
    if (GPSCoord.long >= standardcalc.GPSDistAway(destination, 10, 0).long and gVars.kill_flagRB == 0):# or GPSCoord.long <= standardcalc.GPSDistAway(destination, -10, 0).long) and (GPSCoord.lat >= standardcalc.GPSDistAway(destination, 0, 10).lat or GPSCoord.lat <= standardcalc.GPSDistAway(destination, 0, -10).lat): 
        pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
        GPSCoord.long = gVars.currentData[gps_index].long
        GPSCoord.lat = gVars.currentData[gps_index].lat
        
    # Checks if the boat needs to round the buoy or just pass it
    vect = datatypes.GPSCoordinate()
    vect.lat = BuoyLoc.lat - currentData[gps_index].lat
    vect.long = BuoyLoc.long - currentData[gps_index].long
    
    # Checks if the boat as to round the buoy
    buoyAngle = None
    buoyAngle = standardcalc.vectorToDegrees(vect.lat, vect.long)
    buoyAngle -= 90 
    buoyAngle = standardcalc.boundTo180(buoyAngle) #git later
    
    if FinalBearing < buoyAngle and FinalBearing > standardcalc.boundTo180(buoyAngle - 90):        
        destination = standardcalc.GPSDistAway(GPSCoord, moveLong2, moveLat2)
        
        # 10 represents the degree of error around the destination point
        # Calls point to point function until it reaches location past buoy
        # Adding 10 does not increase the radius by 10 meters(ERROR!) - fixed
        if (GPSCoord.long >= standardcalc.GPSDistAway(destination, 10, 0).long or GPSCoord.long <= standardcalc.GPSDistAway(destination, -10, 0).long) and (GPSCoord.lat >= standardcalc.GPSDistAway(destination, 0, 10).lat or GPSCoord.lat <= standardcalc.GPSDistAway(destination, 0, -10).lat)  and gVars.kill_flagRB == 0: 
            pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
            GPSCoord.long = gVars.currentData[gps_index].long
            GPSCoord.lat = gVars.currentData[gps_index].lat 
    
    return 0
    '''
# --- Round Buoy Stbd---
# Input: Round Buoy location, Final bearing with respect to North
def roundBuoyStbd(BuoyLoc, FinalBearing=None):
    currentData = gVars.currentData
        
    if FinalBearing is None:
        FinalBearing = standardcalc.boundTo180(standardcalc.angleBetweenTwoCoords(currentData[gps_index], BuoyLoc)-179)
        
    GPSCoord = currentData[gps_index]
    appWindAng = currentData[awa_index]
    cog = currentData[cog_index] # Course  over ground    
    hog = currentData[hog_index] # Height over ground
    
    X = 16.64 # Degrees, Calculated
    Dest = 23.41 # Meters, Distance from boat to buoy
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    reflectLong = GPSCoord.long * -1 # Used for calculation ONLY, because longitude decreases from left to right
    quadDir = None
    
    if reflectLong > BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.cos(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat = abs(math.sin(180 - angleToNorth + X)) * - 1 # - Y movement
        quadDir = 3
        moveLong2 = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
        moveLat2 = abs(math.cos(angleToNorth + X)) # + Y Movement 
    elif reflectLong < BuoyLoc.long and GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.sin(angleToNorth -90 - X)) # + X Movement
        moveLat = abs(math.cos(angleToNorth - 90 - X)) * -1 # - Y Movement
        quadDir = 4
        moveLong2 = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat2 = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
    elif reflectLong < BuoyLoc.long and GPSCoord.lat < BuoyLoc.lat:
        moveLong = abs(math.cos(angleToNorth - X)) # + X Movement
        moveLat = abs(math.sin(angleToNorth - X)) # + Y Movement
        quadDir = 1
        moveLong2 = abs(math.cos(angleToNorth -90 - X)) # + X Movement
        moveLat2 = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
    else:
        moveLong = abs(math.sin(angleToNorth - X)) * - 1 # - X Movement
        moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement 
        quadDir = 2
        moveLong2 = abs(math.sin(angleToNorth - X)) # + X Movement
        moveLat2 = abs(math.cos(angleToNorth - X)) # + Y Movement
    
    moveLong *= Dest
    moveLat *= Dest
    
    moveLong *= -1 # Convert back to actual coordinates
    
    destination = standardcalc.GPSDistAway(GPSCoord, moveLong, moveLat)

    # 10 represents the degree of error around the destination point
    # Calls point to point function until it reaches location past buoy
    # Adding 10 does not increase the radius by 10 meters(ERROR!) - fixed 
    if gVars.kill_flagRB == 0:
        pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
    
    # Checks if the boat needs to round the buoy or just pass it
    vect = datatypes.GPSCoordinate()
    vect.lat = BuoyLoc.lat - currentData[gps_index].lat
    vect.long = BuoyLoc.long - currentData[gps_index].long
  
    # Checks if the boat has to round the buoy
    buoyAngle = None
    buoyAngle = standardcalc.vectorToDegrees(vect.lat, vect.long)
    buoyAngle -= 90 
    buoyAngle = standardcalc.boundTo180(buoyAngle) #git later 
    
    if FinalBearing < buoyAngle and FinalBearing > standardcalc.boundTo180(buoyAngle - 90):
        destination = standardcalc.GPSDistAway(GPSCoord, moveLong2, moveLat2)
            
        # 10 represents the degree of error around the destination point
        # Calls point to point function until it reaches location past buoy
        # Adding 10 does not increase the radius by 10 meters(ERROR!) - fixed
        if (GPSCoord.long >= standardcalc.GPSDistAway(destination, 10, 0).long or GPSCoord.long <= standardcalc.GPSDistAway(destination, -10, 0).long) and (GPSCoord.lat >= standardcalc.GPSDistAway(destination, 0, 10).lat or GPSCoord.lat <= standardcalc.GPSDistAway(destination, 0, -10).lat) and gVars.kill_flagRB == 0: 
            pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
            GPSCoord.long = gVars.currentData[gps_index].long
            GPSCoord.lat = gVars.currentData[gps_index].lat 
            
    return 0

def roundBuoy(BuoyLoc, FinalLoc=None, port=True):
    GPSCoord = gVars.currentData[gps_index]
    if FinalLoc == None:
        FinalLoc = GPSCoord
    ANGLE_BOAT_TO_TARGET_WRT_BUOY = 138
    calc = roundBuoyCalc(BuoyLoc, ANGLE_BOAT_TO_TARGET_WRT_BUOY, 10)
    
    X = calc.Angle
    Dest = calc.Dest # Meters, Distance from boat to target (after buoy)
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    move = None
    
    if port:
        move = portCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X)
    else:
        move = starCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X)
                
    move[0].Long *= Dest 
    move[0].Lat *= Dest 
    destination = standardcalc.GPSDistAway(GPSCoord, move[0].Long, move[0].Lat)

    if (GPSCoord.long >= standardcalc.GPSDistAway(destination, 10, 0).long): 
        pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
        
    # Checks if the boat needs to round the buoy or just pass it
    PassBuoyData = gVars.currentData
    angleToTarget = standardcalc.angleBetweenTwoCoords(PassBuoyData[gps_index], FinalLoc)
    angleToBuoy = standardcalc.angleBetweenTwoCoords(PassBuoyData[gps_index], BuoyLoc)
    
    if angleToTarget < standardcalc.boundTo180(angleToBuoy + 15) and angleToTarget > standardcalc.boundTo180(angleToBuoy - 15): 
        destination = standardcalc.GPSDistAway(GPSCoord, move[1].Long, move[1].Lat)
        pointToPoint(datatypes.GPSCoordinate(destination.lat, destination.long),1)
        
    return 0

def portCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X):
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
    
    move = None
    move[0].long = moveLong
    move[0].lat = moveLat
    move[1].long = moveLong2
    move[1].lat = moveLat2
    
    return move

def starCalcRoundBuoy(GPSCoord, BuoyLoc, angleToNorth, X):
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
        
        move = None
        move[0].long = moveLong
        move[0].lat = moveLat
        move[1].long = moveLong2
        move[1].lat = moveLat2
    
    return move

def roundBuoyCalc(BuoyLoc, gamma, DisTargetToBuoy=10):
    currentData = gVars.currentData
    GPSCoord = currentData[gps_index]
    
    DisBoatToBuoy = standardcalc.distBetweenTwoCoords(BuoyLoc, GPSCoord)
    Dest = math.sqrt(DisTargetToBuoy**2 + DisBoatToBuoy**2 - 2*DisTargetToBuoy*DisBoatToBuoy*math.cos(gamma))
    theta2 = 180 - gamma
    x1 = math.cos(theta2)*DisTargetToBuoy
    gVars.logger.info(str((DisBoatToBuoy + x1)/Dest))
    outX = math.acos((DisBoatToBuoy + x1)/Dest)
    
    calc = None
    calc.Angle = outX
    calc.Dest = Dest
    
    return calc
        
def killPointToPoint():
    gVars.kill_flagPTP = 1

# --- Point to Point ---
# Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own, TWA = 0 for sailing using only AWA and 1 for attempting to find TWA.
# Output: Nothing
def pointToPoint(Dest, initialTack = None, ACCEPTANCE_DISTANCE = sVars.ACCEPTANCE_DISTANCE_DEFAULT):
    sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
    tackSailing = 0
    newTackSailing = 0
    gVars.kill_flagPTP = 0
    end_flag = 0
    arduino = gVars.arduino
    appWindAng = 0
    oldColumn = 0
    tackDirection = 0
    gVars.logger.info("Started point to pointAWA")
    
    while(end_flag == 0 and gVars.kill_flagPTP == 0):
        gVars.logger.info("End flag and kill flag OK")
        currentData = gVars.currentData
        GPSCoord = currentData[gps_index]
        newappWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        sog = currentData[sog_index] * 100        
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord, Dest) > ACCEPTANCE_DISTANCE):
            gVars.logger.info("Boat not at point, continuing code")
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            standardcalc.getWeatherSetting(newappWindAng,sog)
                #print ("Hit else statement")
                #print ("TWA is: " + str(gVars.TrueWindAngle))
                                
            if(standardcalc.isWPNoGoAWA(newappWindAng,hog,Dest,sog,GPSCoord)):
                gVars.logger.info("Point cannot be reached directly")
                #Trying to determine whether 45 degrees clockwise or counter clockwise of TWA wrt North is closer to current heading
                #This means we are trying to determine whether hog-TWA-45 or hog-TWA+45 (both using TWA wrt North) is closer to our current heading.
                #Since those values give us TWA wrt to north, we need to subtract hog from them to get TWA wrt to our heading and figure out which one has a smaller value.
                #To get it wrt to current heading, we use hog-TWA-45-hog and hog-TWA+45-hog.  Both terms have hogs cancelling out.
                #We are left with -TWA-45 and -TWA+45, which makes sense since the original TWA was always with respect to the boat.
                #Since we are trying to figure out which one is closest to turn to, we use absolute values.
                if(starboardTackWanted(newappWindAng,initialTack)):
                    newTackSailing = 1
                    initialTack = None
                    gVars.tacked_flag = 0
                    while(doWeStillWantToTack(hog,GPSCoord,Dest)):
                        gVars.logger.info("On starboard tack")
                        
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        newappWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index] * 100  #Using speed in cm/s
                                               
                        standardcalc.getWeatherSetting(newappWindAng, sog)                            
                        
                        if( isThereChangeToAWAorWeatherOrMode(appWindAng,newappWindAng,oldColumn,tackSailing,newTackSailing) ):
                            gVars.logger.info("Changing sheets and rudder")
                            arduino.adjust_sheets(sheetList[abs(int(newappWindAng))][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newappWindAng-TACKING_ANGLE)
                            appWindAng = newappWindAng
                            oldColumn = gVars.currentColumn
                            tackSailing = newTackSailing
                            
                        if(newappWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                        
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    gVars.logger.info("Tacked from boundary")
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                        if(gVars.tacked_flag):
                            break
                        
                    if(gVars.tacked_flag == 0):                                                                
                        arduino.tack(gVars.currentColumn,tackDirection)
                    gVars.logger.info("Tacked from 80 degrees")
                    
                elif(portTackWanted(newappWindAng,initialTack)):
                    newTackSailing = 2
                    initialTack = None
                    gVars.tacked_flag = 0
                    while(doWeStillWantToTack(hog,GPSCoord,Dest)):
                        gVars.logger.info("On port tack")
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        newappWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index]*100
                        
                        standardcalc.getWeatherSetting(newappWindAng,sog)
                        #TWA = abs(int(TWA))
                        #print ("TWA is: " + str(newTWA))
                        
                        if(isThereChangeToAWAorWeatherOrMode(appWindAng,newappWindAng,oldColumn,tackSailing,newTackSailing)):
                            gVars.logger.info("Changing sheets and rudder")
                            arduino.adjust_sheets(sheetList[abs(int(newappWindAng))][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newappWindAng+TACKING_ANGLE)
                            appWindAng = newappWindAng
                            oldColumn = gVars.currentColumn
                            tackSailing = newTackSailing
                            
                        if(newappWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                            
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    gVars.logger.info("Tacked from boundary")
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                        
                        if(gVars.tacked_flag):
                            break
                        
                    if(gVars.tacked_flag == 0):                                                                
                        arduino.tack(gVars.currentColumn,tackDirection)
                    gVars.logger.info("Tacked from 80 degrees")
                    
            else:
                gVars.logger.info("Sailing straight to point")
                newTackSailing = 3
                if(isThereChangeToAWAorWeatherOrMode(appWindAng,newappWindAng,oldColumn,tackSailing,newTackSailing)):
                    gVars.logger.info("Changing sheets and rudder")
                    arduino.adjust_sheets(sheetList[abs(int(newappWindAng))][gVars.currentColumn])
                    arduino.steer(COMPASS_METHOD,standardcalc.angleBetweenTwoCoords(GPSCoord,Dest))
                    appWindAng = newappWindAng
                    oldColumn = gVars.currentColumn
                    tackSailing = newTackSailing
            
        else:
            end_flag = 1
            gVars.logger.info("Finished Point to Point")
    
    return 0

def starboardTackWanted(AWA,initialTack):
    if( (abs(-AWA-TACKING_ANGLE)<abs(-AWA+TACKING_ANGLE) and initialTack is None) or initialTack == 1 ):
        return 1
    else:
        return 0
        
def portTackWanted(AWA,initialTack):
    if( (abs(-AWA-TACKING_ANGLE)>=abs(-AWA+TACKING_ANGLE) and initialTack is None) or initialTack == 0 ):
        return 1
    else:
        return 0

def doWeStillWantToTack(hog,GPSCoord,Dest):
    if(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80 and gVars.kill_flagPTP ==0):
        return 1
    else:
        return 0
    
def isThereChangeToAWAorWeatherOrMode(AWA,newAWA,oldColumn,tackSailing,newTackSailing):
    if(AWA != newAWA or oldColumn != gVars.currentColumn or tackSailing != newTackSailing):
        return 1
    else:
        return 0
