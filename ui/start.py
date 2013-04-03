import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import server
from threading import Thread
from api import ApiControl

print(sys.path)
import control.__main__

runControlCode=True

if runControlCode:
  from control.GuiHandler import GuiHandler
  interface = GuiHandler()
  controlThread = Thread(target=control.__main__.main)
  controlThread.daemon = True
  controlThread.start()
else:
  from simulator import Simulator
  interface = Simulator()

server.apiControl = ApiControl(interface)


try:
  server.app.run()
except KeyboardInterrupt:
  pass

