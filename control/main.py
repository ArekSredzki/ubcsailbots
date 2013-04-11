'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
import logging
import sched
import time
from datetime import datetime
from os import path
from challenge import longdistance
from challenge import navigation
from challenge import stationkeeping
from logic import coresailinglogic
from control import sailbotlogger
from datatype import datatypes
import control.GlobalVars as gVars
import control.StaticVars as sVars
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
    gVars.logger = sailbotlogger.logger()
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
            
        if (len(gVars.functionQueue) > 0 and gVars.currentProcess is None and gVars.currentData[sVars.AUT_INDEX] == 1):
            killAllFunctions()
            time.sleep(.5)
            unkillAllFunctions()
            gVars.currentProcess = gVars.functionQueue.pop(0)
            gVars.currentParams = gVars.queueParameters.pop(0)
            if (gVars.currentProcess == sVars.GO_AROUND_PORT or gVars.currentProcess == sVars.GO_AROUND_STBD or gVars.currentProcess == sVars.GO_TO):
                gVars.taskStartTime = datetime.now()
                try:
                    getattr(coresailinglogic, gVars.currentProcess)(*gVars.currentParams)
                except Exception, errtext:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    gVars.logger.critical("Caught exception in " + str(gVars.currentProcess) + ":<br>" + str(errtext) + "<br> Trace: " + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace('\n', '<br>'+'&nbsp '*3))
            elif (gVars.currentProcess == sVars.NAVIGATION_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                try:
                    navigation.run(*gVars.currentParams)
                except Exception, errtext:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    gVars.logger.critical("Caught exception in " + str(gVars.currentProcess) + ":<br>" + str(errtext) + "<br> Trace: " + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace('\n', '<br>'+'&nbsp '*3))
            elif (gVars.currentProcess == sVars.STATION_KEEPING_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                try:
                    stationkeeping.run(*gVars.currentParams)
                except Exception, errtext:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    gVars.logger.critical("Caught exception in " + str(gVars.currentProcess) + ":<br>" + str(errtext) + "<br> Trace: " + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace('\n', '<br>'+'&nbsp '*3))
            elif (gVars.currentProcess == sVars.LONG_DISTANCE_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                try:
                    longdistance.run(*gVars.currentParams)
                except Exception, errtext:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    gVars.logger.critical("Caught exception in " + str(gVars.currentProcess) + ":<br>" + str(errtext) + "<br> Trace: " + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace('\n', '<br>'+'&nbsp '*3))
            else:
                gVars.logger.warning("No instruction task named " + str(gVars.currentProcess))
            gVars.currentProcess = None
            gVars.currentParams = None
                
        time.sleep(.5)
        

def setGlobVar(sc):
    if gVars.currentProcess == None:
        killAllFunctions()
    gVars.currentData = gVars.arduino.getFromArduino()
    printArdArray(gVars.currentData)
    if (mock):
        sc.enter(1, 1, setGlobVar, (sc,))
    else:
        sc.enter(1, 1, setGlobVar, (sc,))
    
def printArdArray(arr):
    print("Heading: " + str(arr[sVars.HOG_INDEX]) + ", COG: " + str(arr[sVars.COG_INDEX]) + ", SOG: " + str(arr[sVars.SOG_INDEX]) + ", AWA: " + str(arr[sVars.AWA_INDEX]) + ", GPS[" + str(arr[sVars.GPS_INDEX]) + "]" + ", Sheet Percent: " + str(arr[sVars.SHT_INDEX]) + ", Num of Satellites: " + str(arr[sVars.SAT_INDEX]) + ", Accuracy: " + str(arr[sVars.ACC_INDEX]) + ", Rudder: " + str(arr[sVars.RUD_INDEX]))
    
def unkillAllFunctions():
    # All current kill flags must be added here.
    gVars.kill_flagPTP = 0
    gVars.kill_flagNav = 0
    gVars.kill_flagSK = 0
    gVars.kill_flagRB = 0
    gVars.kill_flagLD = 0

def killAllFunctions():
    # All current kill flags must be added here.
    gVars.kill_flagPTP = 1
    gVars.kill_flagNav = 1
    gVars.kill_flagSK = 1
    gVars.kill_flagRB = 1
    gVars.kill_flagLD = 1

if __name__ == '__main__':
    try:
        sys.exit(run())
    except KeyboardInterrupt:
        gVars.logger.info("\n Exit - Keyboard Interrupt")
