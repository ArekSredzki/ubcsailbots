import json
import unittest
import simulator



class Challenge:
    def __init__(self):
        # Declare all public instance variables
        self.challengeName = ""
    
    def setType(self, name):
        self.challengeType = name
        
    def getName(self):
        return self.challengeType
    
    