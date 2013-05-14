'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
import sched
import time
from datetime import datetime
from challenge import longdistance
from challenge import navigation
from challenge import stationkeeping
from challenge import chaserace
from logic import roundbuoy
from logic import pointtopoint
from control import sailbot_logger
import control.global_vars as gVars
import control.static_vars as sVars
import piardio.arduino
import piardio.mockarduino
import traceback

# Mock:
    #   - If true, mock will run from a mock arduino class which simulates boat and wind conditions (see readme)
    #   - If false, mock will run off of an actual arduino through dev/tty ports     
mock = False

# Main - pass challenge or logic function name as argument
def run(argv=None):
    #with open(path.join(path.dirname(__file__),'log/sailbot.log'), 'w'):
    #    pass
    gVars.logger = sailbot_logger.Logger()
    gVars.logger.info("Start")
    
    gVars.logger.info("Mock Enabled: " + str(mock))
    if (mock == False):        
        arduino = piardio.arduino.arduino()
    else:
        arduino = piardio.mockarduino.arduino()
    gVars.logger.info("Created Arduino object")
    gVars.arduino = arduino
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, setGlobVar, (s,))
    thread.start_new_thread(s.run, ())
    
    while (gVars.run):
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        
        #TODO build function calling wrapper like getattr(coresailinglogic, gVars.currentProcess)(*gVars.currentParams)
        if (len(gVars.functionQueue) > 0 and gVars.currentProcess is None and gVars.currentData.auto == 1):
            killAllFunctions()
            time.sleep(.5)
            unkillAllFunctions()
            gVars.currentProcess = gVars.functionQueue.pop(0)
            gVars.currentParams = gVars.queueParameters.pop(0)
            task = getTaskObject(gVars.currentProcess)
            
            gVars.taskStartTime = datetime.now()
            
            try:
                task.run(*gVars.currentParams)
            except Exception, errtext:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                gVars.logger.critical("Caught exception in " + str(gVars.currentProcess) + ":<br>" + str(errtext) + "<br> Trace: " + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace('\n', '<br>'+'&nbsp '*3))
            
            gVars.currentProcess = None
            gVars.currentParams = None
                
        time.sleep(.5)
        
def getTaskObject(process):
    if (process == sVars.GO_AROUND):
        return roundbuoy.RoundBuoy()
    elif (process == sVars.GO_TO):
        return pointtopoint.PointToPoint()
    elif (process == sVars.NAVIGATION_CHALLENGE):
        return navigation.Navigation()
    elif (process == sVars.STATION_KEEPING_CHALLENGE):
        return stationkeeping.StationKeeping()
    elif (process == sVars.LONG_DISTANCE_CHALLENGE):
        return longdistance.LongDistance()
    elif (process == sVars.CHASE_RACE_CHALLENGE):
        return chaserace.ChaseRace()
    else:
        gVars.logger.warning("No instruction task named " + str(process))
    
def setGlobVar(sc):
    if gVars.currentProcess == None:
        killAllFunctions()
    gVars.currentData = gVars.arduino.getFromArduino()
    print gVars.currentData
    if (mock):
        sc.enter(1, 1, setGlobVar, (sc,))
    else:
        sc.enter(1, 1, setGlobVar, (sc,))
        
def unkillAllFunctions():
    # All current kill flags must be added here.
    gVars.kill_flagPTP = 0
    gVars.kill_flagNav = 0
    gVars.kill_flagSK = 0
    gVars.kill_flagRB = 0
    gVars.kill_flagLD = 0
    gVars.kill_flagCR = 0

def killAllFunctions():
    # All current kill flags must be added here.
    gVars.kill_flagPTP = 1
    gVars.kill_flagNav = 1
    gVars.kill_flagSK = 1
    gVars.kill_flagRB = 1
    gVars.kill_flagLD = 1
    gVars.kill_flagCR = 1

if __name__ == '__main__':
    try:
        sys.exit(run())
    except KeyboardInterrupt:
        gVars.logger.info("\n Exit - Keyboard Interrupt")
