'''
Created on Jan 19, 2013

@author: joshandrews
'''

import sys
sys.path.append("..")
from control import static_vars as sVars
from control import global_vars as gVars
from control.logic import pointtopoint
from control.logic import roundbuoy
from control import sailing_task

class LongDistance(sailing_task.SailingTask):
    
    def __init__(self):
        self.pointtopoint = pointtopoint.PointToPoint()
        self.roundbuoy = roundbuoy.RoundBuoy()
    
    def run(self, wayList):
        gVars.logger.info("Running Long Distance")
                
        for waypoint in wayList:
            if gVars.kill_flagLD == 0:
                gVars.logger.info("Heading toward " + waypoint.wtype + " which is mark " + str(wayList.index(waypoint)+1) + " of " + str(len(wayList)+1))
                
                if waypoint.wtype == sVars.GO_AROUND:
                    self.pointtopoint.run(waypoint.coordinate, 30)
                    # Currently will round all buoys port.  May need to be changed for course outline
                    self.roundbuoy.run(waypoint.coordinate)
                else:
                    self.pointtopoint.run(waypoint.coordinate, 20)
                                    
            else:
                break