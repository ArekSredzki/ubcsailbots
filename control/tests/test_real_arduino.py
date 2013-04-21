import sys,os
sys.path.append(os.path.abspath('../../'))

import unittest
from control.piardio import arduino
import time

@unittest.skip("Skip unless connected to Arduino by USB")
class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.ard = arduino.arduino()
    
    def testReturn(self):
        ard = self.ard.getFromArduino()
        print("Heading: " + str(ard.hog) + ", COG: " + str(ard.cog) + ", SOG: " + 
              str(ard.sog) + ", AWA: " + str(ard.awa) + ", GPS[" + str(ard.gps_coord) 
              + "]" + ", Sheet Percent: " + str(ard.sheet_percent) + ", Num of Satellites: " + str(ard.num_sat))
        #self.ard.ser.close()
    
    def testSend(self):
        time.sleep(1)
        self.ard.adjust_sheets(50)
        time.sleep(1)
        self.testReturn()
        self.ard.ser.close() 

if __name__ == '__main__':
    unittest.main()