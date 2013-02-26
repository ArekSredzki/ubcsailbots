import server
import thread
from api import ApiControl


from simulator import Simulator
interface = Simulator()


## uncomment to use control GuiHandler
#import sys, os
#sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'control/'))
#print sys.path
#from control.GuiHandler import GuiHandler
#interface = GuiHandler()


server.apiControl = ApiControl(interface)
thread.start_new_thread(server.app.run())