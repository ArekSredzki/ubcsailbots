#Unit Tests of DataTypes.py Module
import sys, os
sys.path.append(os.path.abspath('../'))
import unittest
import control.datatype.datatypes as datatype
import control.static_vars as sVars

class TestGPSCoordinate(unittest.TestCase):
	def setUp(self):
		self.x = datatype.GPSCoordinate()
		self.y = datatype.GPSCoordinate(42, -121)
	
	def testConstructor(self):
		self.assertEqual(self.x.lat, 0)
		self.assertEqual(self.x.long, 0)
		self.assertEqual(self.y.lat, 42)
		self.assertEqual(self.y.long, -121)

class TestWaypoint(unittest.TestCase):
	def setUp(self):
		self.x = datatype.Waypoint(datatype.GPSCoordinate())
		self.y = datatype.Waypoint(datatype.GPSCoordinate(42, -121), sVars.GO_TO)
	
	def testConstructor(self):
		self.assertEqual(self.x.coordinate.lat, 0)
		self.assertEqual(self.x.coordinate.long, 0)
		self.assertEqual(self.x.wtype, "")
		self.assertEqual(self.y.coordinate.lat, 42)
		self.assertEqual(self.y.coordinate.long, -121)
		self.assertEqual(self.y.wtype, sVars.GO_TO)

class TestBoundary(unittest.TestCase):
	def setUp(self):
		self.x = datatype.Boundary(datatype.GPSCoordinate())
		self.y = datatype.Boundary(datatype.GPSCoordinate(42, -121), 123.456)
	
	def testConstructor(self):
		self.assertEqual(self.x.coordinate.lat, 0)
		self.assertEqual(self.x.coordinate.long, 0)
		self.assertEqual(self.x.radius, 0)
		self.assertEqual(self.y.coordinate.lat, 42)
		self.assertEqual(self.y.coordinate.long, -121)
		self.assertEqual(self.y.radius, 123.456)


class TestArduinoData(unittest.TestCase):
	def setUp(self):
		self.x = datatype.ArduinoData()
		self.y = datatype.ArduinoData(10,10,10,10,datatype.GPSCoordinate(10,10),10,10,10,10,10)
	
	def testConstructor(self):
		self.assertEqual(self.x.sog, 0)
		self.assertEqual(self.x.hog, 0)
		self.assertEqual(self.y.sog, 10)
		self.assertEqual(self.y.hog, 10)
	
	def testRepr(self):
		self.assertEqual(repr(self.x), "ArduinoData(hog=0,cog=0,sog=0,awa=0,gps_coord=GPSCoordinate(latitude=0, longitude=0),sheet_percent=0,num_sat=0,gps_accuracy=0,auto=0,rudder=0)") 	
		self.assertEqual(repr(self.y), "ArduinoData(hog=10,cog=10,sog=10,awa=10,gps_coord=GPSCoordinate(latitude=10, longitude=10),sheet_percent=10,num_sat=10,gps_accuracy=10,auto=10,rudder=10)") 	

if __name__ == '__main__':
	unittest.main()