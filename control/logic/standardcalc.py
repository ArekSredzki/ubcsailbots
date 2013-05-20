'''
Created on Jan 20, 2013

@author: joshandrews
'''
import math
from os import path
from control.datatype import datatypes
from control.parser import parsing
from control import static_vars as sVars
from control import global_vars as gVars

EARTH_RADIUS = 6378140.0

#returns gpscoordinate distance in meters away from starting point.
#positive yDist = North, positive xDist = East
def GPSDistAway(coord, xDist, yDist):
    result = datatypes.GPSCoordinate()
    result.long = coord.long + (180.0/math.pi)*(float(xDist)/EARTH_RADIUS)/math.cos(math.radians(coord.lat))
    result.lat = coord.lat + (180.0/math.pi)*(float(yDist)/EARTH_RADIUS)
    return result

def setBoxCoords(p0, p1, p2, p3): #sets box coords in order going around the box
    case=[]
    case.append([p0,p1,p2,p3])
    # 0-----3
    # |     |
    # |     |
    # 1-----2
    
    case.append([p0,p1,p3,p2])
    # 0     3
    # | \ / |
    # | / \ |
    # 1     2
    
    case.append([p0,p3,p1,p2])
    # 0-----3
    #   \ / 
    #   / \ 
    # 1-----2
    
    # if the points are connected in a square then the sum of angles is 360
    # otherwise the sum will be <360 and the points are connected wrong
    angleSums=[]
    for c in case:
        angleSums.append(sumCornerAngles(c))
    caseNumber = angleSums.index(max(angleSums))
    boxList = case[caseNumber]
    
    return makeClockWise(boxList)
  
def makeClockWise(boxList):
    angle1 = angleBetweenTwoCoords(boxList[0],boxList[1])
    angle2 = angleBetweenTwoCoords(boxList[0],boxList[3])
    delta = calculateAngleDelta(angle1, angle2)
    if delta <0:
        return boxList
    else:
        return [boxList[3],boxList[2],boxList[1],boxList[0]]
def sumCornerAngles(coordList):
    sum=angleBetweenThreePoints(coordList[0],coordList[1],coordList[2])
    sum+=angleBetweenThreePoints(coordList[1],coordList[2],coordList[3])
    sum+=angleBetweenThreePoints(coordList[2],coordList[3],coordList[0])
    sum+=angleBetweenThreePoints(coordList[3],coordList[0],coordList[1])
    return sum
def angleBetweenThreePoints(p2,p1,p3):
    #cosine rule around point p2
    p12=distBetweenTwoCoords(p1,p2)
    p13=distBetweenTwoCoords(p1,p3)
    p23=distBetweenTwoCoords(p2,p3)
    return findCosLawAngle(p12,p13,p23)
  
#Returns the distance in metres
def distBetweenTwoCoords(coord1, coord2):
    dLongRad = math.radians(coord1.long - coord2.long)
    dLatRad = math.radians(coord1.lat - coord2.lat)
    latRad1 = math.radians(coord1.lat)
    latRad2 = math.radians(coord2.lat)
    
    a = math.pow(math.sin(dLatRad/2),2) + math.cos(latRad1)*math.cos(latRad2)*math.pow(math.sin(dLongRad/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return EARTH_RADIUS*c

#Returns the angle in degrees
def angleBetweenTwoCoords(sourceCoord, destCoord):
    GPSCoord = datatypes.GPSCoordinate()
    
    if(sourceCoord.lat > destCoord.lat):
        GPSCoord.lat = sourceCoord.lat
        GPSCoord.long = destCoord.long
    
    elif(sourceCoord.lat < destCoord.lat):
        GPSCoord.lat = destCoord.lat
        GPSCoord.long = sourceCoord.long
    
    elif(sourceCoord.long < destCoord.long):
        return 90
    
    elif(sourceCoord.long > destCoord.long):
        return -90
    
    else:
        return None
    
    
    distBtwnCoords = distBetweenTwoCoords(sourceCoord, destCoord)
    distSin = distBetweenTwoCoords(destCoord, GPSCoord)
        
    angle = math.asin(distSin/distBtwnCoords)*180/math.pi
    
    if(sourceCoord.lat < destCoord.lat):
        if(sourceCoord.long < destCoord.long):
            return angle
        elif(sourceCoord.long > destCoord.long):
            angle = -angle
            return angle
        else:
            return 0        
    else:
        if(sourceCoord.long < destCoord.long):
            angle = 90+angle
            return angle
        elif(sourceCoord.long > destCoord.long):
            angle = -90-angle
            return angle
        else:
            return 180

#Determines whether the waypoint can be reached with our current coordinates using AWA
#Returns 1 if waypoint can't be reached
#Returns 0 if waypoint can be reached
def isWPNoGoAWA (AWA, hog, dest, sog, GPS):    
    if(sog < sVars.SPEED_AFFECTION_THRESHOLD):
        if(isAngleBetween(hog+AWA-45,angleBetweenTwoCoords(GPS,dest),hog+AWA+45)):
            return 1
        else:
            return 0
    else:
        if(isAngleBetween(hog+AWA-30,angleBetweenTwoCoords(GPS,dest),hog+AWA+30)):
            return 1
        else:
            return 0

def getTrueWindAngle(awa, sog):
    sVars.AWA_THRESHOLD = 0.9
    while(1):
        sVars.SOG_THRESHOLD = 0.9
        while(1):
            AWAList = parsing.parse(path.join(path.dirname(__file__), 'AWA.txt'))
            SOGList = parsing.parse(path.join(path.dirname(__file__), 'SOGarray'))
            AWAentries = searchAWAIndex(awa, AWAList)
            SOGentries = searchSOGIndex(sog, SOGList)
        
            for i in range(len(AWAentries)):
                index = AWAentries[i][0]
                column = AWAentries[i][1]
                    
                for x in range(len(SOGentries)):
                    if (SOGentries[x][0] == index) and (SOGentries[x][1] == column):
                        gVars.currentColumn = column
                        if(awa < 0):
                            gVars.trueWindAngle = -index
                        else:
                            gVars.trueWindAngle = index       
                        sVars.SOG_THRESHOLD = 0.9                 
                        return index
            
            sVars.SOG_THRESHOLD += 10
            
            if(sVars.SOG_THRESHOLD >= 500):
                print ("Hit Threshold")
                break
            
        sVars.AWA_THRESHOLD += 1
        
        if(sVars.AWA_THRESHOLD >= 100):
            return None  

def updateWeatherSetting(awa, sog):
    minIndex = 0
    minNum = 500
    SOGList = parsing.parse(path.join(path.dirname(__file__), 'SOGarray'))
    index = boundTo180(awa)
    SOGrow = SOGList[abs(int(index))]
    
    for i in range(len(SOGrow)):
        if(abs(SOGrow[i]-sog)<minNum):
            minIndex = i
            minNum = abs(SOGrow[i]-sog)
            
    gVars.currentColumn = minIndex
        

# takes in a list of speeds. Deletes first element and appends the current speed to the end
def changeSpdList(spdList):
    if (len(spdList) == 0):
        return -1
    del spdList[0]
    spdList.append(gVars.currentData.sog)
    return spdList

def meanOfList(numberList):
    if len(numberList) == 0:
        return -1
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

#Only works with tables with 4 columns!!!!!        
def searchAWAIndex(number, list1):
    number = abs(number)
    big_list = list()
    indcol_list = list()
    
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            big_list.append(list1[i][j])    
    
    for n in range(len(big_list)):
        if( math.fabs(big_list[n]-number) <= sVars.AWA_THRESHOLD ):
            index = math.floor(n/4)
            column = n%4
            small_list = [index,column]
            indcol_list.append(small_list)
            
    return indcol_list

def searchSOGIndex(numberSOG, list1SOG):
    numberSOG = abs(numberSOG)
    big_listSOG = list()
    indcol_listSOG = list()
    
    for i in range(len(list1SOG)):
        for j in range(len(list1SOG[i])):
            big_listSOG.append(list1SOG[i][j])    
    
    for n in range(len(big_listSOG)):
        if( math.fabs(big_listSOG[n]-numberSOG) <= sVars.SOG_THRESHOLD ):
            indexSOG = math.floor(n/4)
            columnSOG = n%4
            small_listSOG = [indexSOG,columnSOG]
            indcol_listSOG.append(small_listSOG)
            
    return indcol_listSOG

#Convert a vector to degrees with respect to North
def vectorToDegrees(x, y):
    if(x >= 0 and y >= 0):
        return math.tan(x/y)*180/3.14159
    elif(x < 0 and y > 0):
        return 90 - math.tan(x/y)*180/3.14159
    elif(x < 0 and y < 0):
        return 180 - math.tan(x/y)*180/3.14159
    else:
        return 90 + math.tan(x/y)*180/3.14159
    
def findCosLawAngle(a, b, c):  #cos law: c^2 = a^2 + b^2 - 2*a*b*cos(theta), returns in RADIANS:
    if ((a < 1) or (b < 1) or (c < 1)):
        return 0
    return math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2*a*b))

# Bounds angle to -180 to 180
def boundTo180(angle):
    if angle < 0:
        angle = angle%-360
    else:
        angle = angle%360
        
    if (angle <= -180):
        return angle+360
    elif (angle > 180):
        return angle-360
    else:
        return angle
    
def boundTo360(angle):
    if (angle < 0):
        return (angle%-360)+360
    elif (angle > 360):
        return angle % 360
    else:
        return angle
    
def SquareRT(a,posFlag):
    if(posFlag==0):
        return -math.sqrt(a)
    else:
        return math.sqrt(a)
    
def isAngleBetween(firstAngle, middleAngle, secondAngle):
    firstAngle = boundTo180(firstAngle)
    middleAngle = boundTo180(middleAngle)
    secondAngle = boundTo180(secondAngle)
    delta1 = calculateAngleDelta(firstAngle, middleAngle)
    delta2 = calculateAngleDelta(middleAngle,secondAngle)
    if abs(delta1+delta2)>=180:
        return False
    elif (delta1>0 and delta2>0):
        return True
    elif (delta1<0 and delta2<0):
        return True
    else:
        return False

def calculateAngleDelta(angle1, angle2):
    difference = angle1-angle2
    if difference >180:
        difference-=360
    if difference <-180:
        difference+=360
    return difference
  
def returnMidPoint(point1, point2):
    return datatypes.GPSCoordinate( (point1.lat +point2.lat)/2.0, (point1.long +point2.long)/2.0)
  
def returnClosestWaypointIndex(coords):
    distances=[]
    for coord in coords:
        dist = distBetweenTwoCoords(gVars.currentData.gps_coord, coord)
        distances.append(dist)
    
    index = distances.index(min(distances))
    return index
