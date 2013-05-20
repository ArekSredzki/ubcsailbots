from control.logic import standardcalc

class TackEngine:

    def hitLayLine(self, HOG, bearing, layAngle):
        angleDelta = abs(standardcalc.calculateAngleDelta(HOG,bearing))
        return angleDelta > layAngle

    def beatEstablished(self, AWA):
        beatingAWATarget = 30
        beatingAWAAcceptanceDelta = 10   
        absoluteAWADelta = abs(  abs(AWA) - beatingAWATarget  )
        return  absoluteAWADelta < beatingAWAAcceptanceDelta

    def onStarboardTack(self,AWA):
        return AWA>=0
            
    def onPortTack(self,AWA):
        return AWA<0
    
    # Sets 1, or 0 for Arduino Call to Tack
    def getTackDirection(self, AWA):
        if(AWA > 0):
            return 1
        else:
            return 0
          
    def canLayMarkWithoutTack(self, AWA, hog, Dest, sog, GPSCoord):
        if standardcalc.isWPNoGoAWA(self.AWA, self.hog, self.Dest,self.sog,self.GPSCoord):
            return False
        else:
            windDirection = standardcalc.boundTo180(self.AWA + self.hog)
            bearing = standardcalc.angleBetweenTwoCoords(self.GPSCoord,self.Dest)
            return not standardcalc.isAngleBetween(bearing,windDirection,self.hog)      
              