'''
Created on May 13, 2013

@author: David Lee
'''
from control import sailing_task
from control.logic import standardcalc
from control import global_vars as gVars
from control.logic import roundbuoychaserace

class ChaseRace(sailing_task.SailingTask):

    def __init__(self):
        pass

    def run(self, wayList):
        self.initialize(wayList[0].coordinate, wayList[1].coordinate, wayList[2].coordinate, wayList[3].coordinate)
        self.race()

    def initialize(self,c0, c1, c2, c3):
        self.roundBuoyCR = roundbuoychaserace.RoundBuoyChaseRace()
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
            self.roundBuoyCR.run(self.boxCoords[self.currentWaypoint])
            self.currentWaypoint = self.getNextWptIndex(self.currentWaypoint)
            gVars.logger.info("Current Waypoint is "+str(self.currentWaypoint))
        gVars.logger.info("ChaseRace Kill Flag initialized. ChaseRace has been stopped.")
