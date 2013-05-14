'''
Created on May 13, 2013

@author: David Lee
'''
from control import sailing_task
from control.logic import standardcalc
from control import global_vars as gVars
from control.logic import roundbuoy

class ChaseRace(sailing_task.SailingTask):
    
    def __init__(self):
        pass

    def run(self,wpt0, wpt1, wpt2, wpt3):
        self.initialize(wpt0.coordinate, wpt1.coordinate, wpt2.coordinate, wpt3.coordinate)
        self.race()

          
    def initialize(self,c0, c1, c2, c3):
        self.roundbuoy = roundbuoy.RoundBuoy()
        self.boxCoords = standardcalc.setBoxCoords(c0, c1, c2, c3)
        self.currentWaypoint = self.getStartDirection(self.boxCoords)
        gVars.logger.info("Current Waypoint is "+str(self.currentWaypoint))
    
    
    def getStartDirection(self, boxCoords):
      index = standardcalc.returnClosestWaypointIndex(boxCoords)
      return self.getNextWptIndex(index)
         
         
    def getNextWptIndex(self,index):
      if gVars.instructions.rounding == "port":
          return (index -1)%4
      else:
          return (index +1)%4 
    
    def race(self):
        while (gVars.kill_flagCR==0):            
            self.roundbuoy.run(self.boxCoords[self.currentWaypoint])
            self.currentWaypoint = self.getNextWptIndex(self.currentWaypoint)
            gVars.logger.info("Current Waypoint is "+str(self.currentWaypoint))
        gVars.logger.info("ChaseRace Kill Flag initialized. ChaseRace has been stopped.")

          