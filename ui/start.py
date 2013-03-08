import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'control/'))

import server
from threading import Thread
from api import ApiControl

print(sys.path)
import control.__main__

runControlCode=True

if runControlCode:
  from control.GuiHandler import GuiHandler
  interface = GuiHandler()
  Thread(target=control.__main__.main, args=()).start()
else:
  from simulator import Simulator
  interface = Simulator()


server.apiControl = ApiControl(interface)
Thread(target=server.app.run, args=()).start()
