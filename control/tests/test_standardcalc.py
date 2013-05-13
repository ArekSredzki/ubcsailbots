#Unit tests of standardcalc.py module
import sys, os
sys.path.append(os.path.abspath('../'))
import unittest
import math

from control.logic import standardcalc
from control.datatype import datatypes
from control import global_vars as gVars

class TestSetBoxCoords(unittest.TestCase):
    def setUp(self):
        self.coord0 = datatypes.GPSCoordinate(1.0,3.0)
        self.coord1 = datatypes.GPSCoordinate(1.0,2.0)
        self.coord2 = datatypes.GPSCoordinate(2.0,2.0) #square
        self.coord3 = datatypes.GPSCoordinate(2.0,3.0)
        
    def testCase1(self):
        self.coordlist1 = standardcalc.setBoxCoords(self.coord0, self.coord1, self.coord2, self.coord3)        
        self.assertIs(self.coordlist1[0],self.coord0)
        self.assertIs(self.coordlist1[1],self.coord1)
        self.assertIs(self.coordlist1[2],self.coord2)
        self.assertIs(self.coordlist1[3],self.coord3)
    def testCase2(self):
        self.coordlist1 = standardcalc.setBoxCoords(self.coord0, self.coord1, self.coord3, self.coord2)        
        self.assertIs(self.coordlist1[0],self.coord0)
        self.assertIs(self.coordlist1[1],self.coord1)
        self.assertIs(self.coordlist1[2],self.coord2)
        self.assertIs(self.coordlist1[3],self.coord3)  
    def testCase3(self):
        self.coordlist1 = standardcalc.setBoxCoords(self.coord0, self.coord2, self.coord1, self.coord3)        
        self.assertIs(self.coordlist1[0],self.coord1)
        self.assertIs(self.coordlist1[3],self.coord0)
        self.assertIs(self.coordlist1[2],self.coord3)
        self.assertIs(self.coordlist1[1],self.coord2)
                          
class TestangleBetweenThreePoints(unittest.TestCase):
    def setUp(self):
        self.coord0 = datatypes.GPSCoordinate(1.0,3.0)
        self.coord1 = datatypes.GPSCoordinate(2.0,3.0)
        self.coord2 = datatypes.GPSCoordinate(2.0,2.0)#90 degrees
    def testAngle(self):
        self.assertAlmostEqual(standardcalc.angleBetweenThreePoints(self.coord0,self.coord1,self.coord2),math.radians(90),places=3)
class TestGPSDistAway(unittest.TestCase):
    def setUp(self):
        self.source = datatypes.GPSCoordinate(49.262330, -123.248148)
        self.result1 = datatypes.GPSCoordinate(49.26322919993, -123.24677409844) #100m north, 100m east
        self.result2 = datatypes.GPSCoordinate(49.26143080008, -123.24952185164) #100m south, 100m west
        self.result3 = datatypes.GPSCoordinate(49.27132080213, -123.23440919997) #1km north, 1km east
        self.result4 = datatypes.GPSCoordinate(49.25333758688, -123.26188680003) #1km south, 1km west
    def testGPSCalc1(self):
        self.test1 = standardcalc.GPSDistAway(self.source, 100, 100)
        self.test2 = standardcalc.GPSDistAway(self.source, -100, -100)
        self.assertEqual((math.fabs(self.result1.lat - self.test1.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result1.long - self.test1.long) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result2.lat - self.test2.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result2.long - self.test2.long) <= 0.00004),1)
    def testGPSCalc2(self):
        self.test3 = standardcalc.GPSDistAway(self.source, 1000, 1000)
        self.test4 = standardcalc.GPSDistAway(self.source, -1000, -1000)
        self.assertEqual((math.fabs(self.result3.lat - self.test3.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result3.long - self.test3.long) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result4.lat - self.test4.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result4.long - self.test4.long) <= 0.00004),1)
    def testGPSCalc3(self):
        self.test5 = standardcalc.GPSDistAway(self.source, 0, 0)
        self.assertEqual(self.test5.lat, self.source.lat)
        self.assertEqual(self.test5.long, self.source.long)
        
class TestDistBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.point1 = datatypes.GPSCoordinate(0,0)
        self.point2 = datatypes.GPSCoordinate(1,1)
        
    def testDist1(self):
        distance = standardcalc.distBetweenTwoCoords(self.point1, self.point2)
        self.assertEqual(round(distance/1000,1), 157.4)
        
class TestAngleBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.source1 = datatypes.GPSCoordinate(100,100)
        self.dest1 = datatypes.GPSCoordinate(300,100)
        
        self.angle1 = standardcalc.angleBetweenTwoCoords(self.source1, self.dest1)
        self.angle2 = standardcalc.angleBetweenTwoCoords(self.dest1, self.source1)
        
        self.source2 = datatypes.GPSCoordinate(0,0)
        self.dest2 = datatypes.GPSCoordinate(1,1)
        
        self.angle3 = standardcalc.angleBetweenTwoCoords(self.source2, self.dest2)
        self.angle4 = standardcalc.angleBetweenTwoCoords(self.dest2, self.source2)
        
        
    def testAngleSet1(self):        
        self.assertEqual(self.angle1, 0)
        self.assertEqual(self.angle2, 180)
        
    def testAngleSet2(self):
        self.assertEqual(round(self.angle3,0), 45)
        self.assertEqual(round(self.angle4,0), -135)
        
class TestSearchAWAIndex(unittest.TestCase):
    def setUp(self):
        self.list1 = [0,1,2,3]
        self.list2 = [0,1,2,3]
        self.big_list = list()
        self.big_list = [self.list1,self.list2]
        self.value1 = 2
        self.value2 = 2.3
        self.value3 = 20
        
    def testSearch1(self):
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[1][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[1][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[1][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[1][1], 3)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[2][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[2][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[3][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[3][1], 3)
        
class TestSearchSOGIndex(unittest.TestCase):
    def setUp(self):
        self.list1 = [0,1,2,3]
        self.list2 = [0,1,2,3]
        self.big_list = list()
        self.big_list = [self.list1,self.list2]
        self.value1 = 2
        self.value2 = 2.3
        self.value3 = 20
        
    def testSearchSOG1(self):
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[1][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[1][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[1][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[1][1], 3)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[2][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[2][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[3][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[3][1], 3)

class TestGetTrueWindAngle(unittest.TestCase):
    def setUp(self):
        self.sog1 = 127
        self.awa1 = 95
        
        self.TWA1 = standardcalc.getTrueWindAngle(self.awa1, self.sog1)
        
    def testGetTrueWindAngle1(self):
        self.assertEqual(self.TWA1, 141)
        
class TestFindCosLawAngle(unittest.TestCase):
    def testFindCosLawAngle(self):
        self.assertEqual(standardcalc.findCosLawAngle(0,1,2),0)
        self.assertEqual(standardcalc.findCosLawAngle(1,-1,2),0)
        self.assertEqual((standardcalc.findCosLawAngle(2,3,4) - 104.477) <=0.001, 1)
    
class TestMeanOfList(unittest.TestCase):
    def setUp(self):
        self.list1 = []
        self.list2 = [1,2,3,4]
        self.list3 = [-0.2, 0, 0.7, 0.9]
        self.list4 = [2]
        
    def testMeanofList1(self):
        self.assertEqual(standardcalc.meanOfList(self.list1), -1)
        self.assertEqual(standardcalc.meanOfList(self.list2), 2.5)
        self.assertEqual(standardcalc.meanOfList(self.list3), 0.35)
        self.assertEqual(standardcalc.meanOfList(self.list4), 2)
        
class TestChangeSpdList(unittest.TestCase):
    def setUp(self):
        self.list1 = []
        gVars.currentData = datatypes.ArduinoData(0, 1, 2, 3, datatypes.GPSCoordinate(4, 4) , 5, 6, 7, 0, 20)
        self.list2 = [1,2,3]
        self.list3 = standardcalc.changeSpdList(self.list2)
        
    def testChangeSpdList1(self):
        self.assertEqual(standardcalc.changeSpdList(self.list1), -1)
        self.assertEqual(self.list3[0] != 1, 1)
        self.assertEqual(self.list3[2] == gVars.currentData.sog, 1)

class TestIsWpnNoGo(unittest.TestCase):
    def setUp(self):
        self.appWind = 131
        self.heading = -30
        self.GPSCoord = datatypes.GPSCoordinate(49,-123)
        self.Dest = datatypes.GPSCoordinate(48.9,-123.1)
        self.sog = 0
        
    def testExpectNotNoGo(self):
        self.assertFalse(standardcalc.isWPNoGoAWA(self.appWind, self.heading, self.Dest, self.sog, self.GPSCoord))
    def testExpectNoGo(self):
        self.appWind=-131
        self.assertTrue(standardcalc.isWPNoGoAWA(self.appWind, self.heading, self.Dest, self.sog, self.GPSCoord))

    
        
class TestBoundto180(unittest.TestCase):
    def setUp(self):
        self.num1 = 5
        self.num1bounded = 5
        self.num2 = 200
        self.num2bounded = -160
        self.num3 = -200
        self.num3bounded = 160
        self.num4 = 890
        self.num4bounded = 170
        self.num5 = 920
        self.num5bounded = -160
        self.num6 = -890
        self.num6bounded = -170
        self.num7 = -920
        self.num7bounded = 160
    
    def testNoChange(self):
        self.assertEqual(standardcalc.boundTo180(self.num1), self.num1bounded)
    
    def testGreaterThan180(self):
        self.assertEqual(standardcalc.boundTo180(self.num2), self.num2bounded)
    
    def testLessThan180(self):
        self.assertEqual(standardcalc.boundTo180(self.num3), self.num3bounded)
    
    def testGreaterThan360ToPositive(self):
        self.assertEqual(standardcalc.boundTo180(self.num4), self.num4bounded)
        
    def testGreaterThan360ToNegative(self):
        self.assertEqual(standardcalc.boundTo180(self.num5), self.num5bounded)
    
    def testLessThan360ToNegative(self):
        self.assertEqual(standardcalc.boundTo180(self.num6), self.num6bounded)
        
    def testLessThan360ToPositive(self):
        self.assertEqual(standardcalc.boundTo180(self.num7), self.num7bounded)

class TestBoundto360(unittest.TestCase):
    def setUp(self):
        self.num1 = 5
        self.num1bounded = 5
        self.num2 = 200
        self.num2bounded = 200
        self.num3 = -200
        self.num3bounded = 160
        self.num4 = 890
        self.num4bounded = 170
        self.num5 = 920
        self.num5bounded = 200
        self.num6 = -890
        self.num6bounded = 190
        self.num7 = -920
        self.num7bounded = 160
    
    def testNoChange(self):
        self.assertEqual(standardcalc.boundTo360(self.num1), self.num1bounded)
    
    def testGreaterThan180(self):
        self.assertEqual(standardcalc.boundTo360(self.num2), self.num2bounded)
    
    def testLessThan180(self):
        self.assertEqual(standardcalc.boundTo360(self.num3), self.num3bounded)
    
    def testGreaterThan360(self):
        self.assertEqual(standardcalc.boundTo360(self.num4), self.num4bounded)
        
    def testGreaterThan360ToAbove180(self):
        self.assertEqual(standardcalc.boundTo360(self.num5), self.num5bounded)
    
    def testLessThanNegative360(self):
        self.assertEqual(standardcalc.boundTo360(self.num6), self.num6bounded)
        
    def testLessThanNegative360More(self):
        self.assertEqual(standardcalc.boundTo360(self.num7), self.num7bounded)
        
class TestBoundAngleDelta(unittest.TestCase):
    def setUp(self):
      pass
    
    def testTwoPossitveAngles(self):
        angle1=50
        angle2=20
        self.assertEqual(standardcalc.calculateAngleDelta(angle1,angle2),30)
    def testTwoNegativeAngles(self):
        angle1=-50
        angle2=-20
        self.assertEqual(standardcalc.calculateAngleDelta(angle1,angle2),-30)
    def testPosAndNegAngles(self):
        angle1=-50
        angle2=20
        self.assertEqual(standardcalc.calculateAngleDelta(angle1,angle2),-70)        
    def testWrapAround180(self):
        angle1=150
        angle2=-150
        self.assertEqual(standardcalc.calculateAngleDelta(angle1,angle2),-60)        
    def testWrapAround180SwapSigns(self):
        angle1=-150
        angle2=150
        self.assertEqual(standardcalc.calculateAngleDelta(angle1,angle2),60)        
