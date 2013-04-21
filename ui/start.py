import sys, os
sys.path.append(os.path.abspath('../'))
print(sys.path)

import server
from threading import Thread
from api import ApiControl

runControlCode=True

if runControlCode:
  import control.main
  from control.gui_handler import GuiHandler
  interface = GuiHandler()
  controlThread = Thread(target=control.main.run)
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

