'''
Created on Jan 20, 2013

@author: joshandrews
'''
import sys, os
sys.path.append(os.path.abspath('../'))
import unittest
import serial
from control.piardio import arduino
from control.datatype import datatypes
from mock import MagicMock

class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.returnstr = "\n1, 22222222, 33333333, 4, 5, 6, 7, 8, 9, 10, 11, 12 \n1, 22222222, 33333333, 4, 5, 6, 7, 8, 9, 10, 11, 12 \n1, 22222222, 33333333, 4, 5, 6, 7, 8, 9, 10, 11, 12"
        self.returnarr = [1, 22222222, 33333333, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.returnstrnospace = "\n1,22222222,33333333,4,5,6,7,8,9,10,11,12\n1,22222222,33333333,4,5,6,7,8,9,10,11,12\n1,22222222,33333333,4,5,6,7,8,9,10,11,12"
        self.arduinoData = datatypes.ArduinoData(5.0, 4.0, 11.0, 7.0, datatypes.GPSCoordinate(3.3333333, 2.2222222), 8.0, 9.0, 10.0, 1.0, 12.0)
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.Serial = MagicMock(return_value=None)
        self.ser.flushInput = MagicMock(return_value=None)
        self.ard = arduino.arduino()
        
    def testNoReturn(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=None)
        self.assertEqual(self.ard.getFromArduino(), None)
        
    def testWithReturn(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=self.returnstr)
        self.assertEqual(self.ard.getFromArduino(), self.arduinoData)
                
    def testWithReturnNoSpace(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=self.returnstrnospace)
        self.assertEqual(self.ard.getFromArduino(), self.arduinoData)
        
if __name__ == '__main__':
    unittest.main()