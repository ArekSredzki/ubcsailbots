'''
Created on Apr 14, 2013

@author: joshandrews
'''

from control import global_vars as gVars

class SailingTask:
    def __init__(self):
        pass
    
    def run(self):
        gVars.logger.error("Subclass must implement abstract method")
        raise NotImplementedError("Subclass must implement abstract method")