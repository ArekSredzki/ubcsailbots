
class GPSCoordinate:
	#This class will be a python representation of GPS coordinates
	#ie with a latitude/longitude made up of "Coordinates"
	#the class should support coordinate operations similar to vector
	#operations, ie GPSCoord1 - GPSCoord2 = A direction and magnitude
	#from one coordinate to the other.
	def __init__(self, latitude=0, longitude=0):
		self.lat = latitude
		self.long = longitude
		
	def __repr__(self):
		return str("GPSCoordinate(latitude={lat}, longitude={long})".format(lat=self.lat, long=self.long))
	
	def __str__(self):
		return str("{lat}, {long}".format(lat=self.lat, long=self.long))
	
	def __eq__(self, other):
		return (self.lat == other.lat and self.long == other.long)

# Instantiates a waypoint for interpretation by the control logic
class Waypoint:
	def __init__(self, coordinate, wtype=""):
		self.coordinate = coordinate
		self.wtype = wtype
	
	def __repr__(self):
		return "Waypoint(coordinate=%r,wtype=%r)" % (self.coordinate,self.wtype)
	
	def __eq__(self, other):
		return (self.coordinate == other.coordinate and self.wtype == other.wtype)


# Instantiates a circular boundary set by a GPS Coordinate and a radius
class Boundary:
	def __init__(self, coordinate, radius=0):
		self.coordinate = coordinate
		self.radius = radius
	
	def __repr__(self):
		return "Boundary(coordinate=%r,radius=%r)" % (self.coordinate,self.radius)
	
	def __eq__(self, other):
		return repr(self) == repr(other)

# Instructions which contain all instructions passed from a GUI to the control logic
class Instructions:
	def __init__(self, challenge, waypoints, boundaries,rounding):
		self.challenge = challenge
		self.waypoints = waypoints
		self.boundaries = boundaries
		self.rounding = rounding
	
	def __repr__(self):
		return "Instructions(challenge=%r,waypoints=%r,boundaries=%r)" % (self.challenge,self.waypoints,self.boundaries)
	
	def __eq__(self, other):
		return repr(self) == repr(other)

class ArduinoData:
	def __init__(self, hog=0, cog=0, sog=0, awa=0, gps_coord=GPSCoordinate(0, 0), sheet_percent=0, num_sat=0, gps_accuracy=0, auto=0, rudder=0):
		self.hog = hog
		self.cog = cog
		self.sog = sog
		self.awa = awa
		self.gps_coord = gps_coord
		self.sheet_percent = sheet_percent
		self.num_sat = num_sat
		self.gps_accuracy = gps_accuracy
		self.auto = auto
		self.rudder = rudder
		
	def __repr__(self):
		return "ArduinoData(hog=%r,cog=%r,sog=%r,awa=%r,gps_coord=%r,sheet_percent=%r,num_sat=%r,gps_accuracy=%r,auto=%r,rudder=%r)" % (self.hog, self.cog, self.sog, self.awa, self.gps_coord, self.sheet_percent, self.num_sat, self.gps_accuracy, self.auto, self.rudder)
	
	def __str__(self):
		return "Heading: " + str(self.hog) + ", COG: " + str(self.cog) + ", SOG: " + str(self.sog) + ", AWA: " + str(self.awa) + ", GPS[" + str(self.gps_coord) + "]" + ", Sheet Percent: " + str(self.sheet_percent) + ", Num of Satellites: " + str(self.num_sat) + ", Accuracy: " + str(self.gps_accuracy) + ", Rudder: " + str(self.rudder)
	
	def __eq__(self, other):
		return (repr(self) == repr(other))
	
	
if (__name__ == "__main__"):
	print "DataTypes.py"