'''
Created on Apr 29, 2013

@author: joshandrews
'''
import unittest
from control import sailbot_logger

class TestSailbotLogger(unittest.TestCase):
    def setUp(self):
        self.logger = sailbot_logger.Logger()
    
    def testLogInfo(self):
        self.testString = "Test Sailbot Logger"
        self.testResponseStringInfo = "[INFO]:Test Sailbot Logger"
        self.logger.info(self.testString)
        self.assertTrue(self.testResponseStringInfo in self.logger.buffer)
    
    def testClearBuffer(self):
        self.testLogInfo()
        self.logger.clearBuffer()
        self.assertEqual(self.logger.buffer, "")