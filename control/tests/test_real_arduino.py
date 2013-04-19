import sys,os
sys.path.append(os.path.abspath('../../'))

import unittest
import serial as ser
from control.piardio import arduino
import control.StaticVars as sVars
import time

@unittest.skip("Skip unless connected to Arduino by USB")
class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.ard = arduino.arduino()
    
    def testReturn(self):
        arr = self.ard.getFromArduino()
        print("Heading: " + str(arr[sVars.HOG_INDEX]) + ", COG: " + str(arr[sVars.COG_INDEX]) + ", SOG: " + 
              str(arr[sVars.SOG_INDEX]) + ", AWA: " + str(arr[sVars.AWA_INDEX]) + ", GPS[" + str(arr[sVars.GPS_INDEX]) 
              + "]" + ", Sheet Percent: " + str(arr[sVars.SHT_INDEX]) + ", Num of Satellites: " + str(arr[sVars.SAT_INDEX]))
        #self.ard.ser.close()
    
    def testSend(self):
        time.sleep(1)
        self.ard.adjust_sheets(50)
        time.sleep(1)
        self.testReturn()
        self.ard.ser.close() 

if __name__ == '__main__':
    unittest.main()