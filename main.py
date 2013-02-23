import ui.server
import thread
from ui.api import ApiControl


from ui.simulator import Simulator
interface = Simulator()


## uncomment to use control GuiHandler 
#import sys, os
#sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'ubcsailbots/control/'))
##print sys.path
#from control.GuiHandler import GuiHandler
#interface = GuiHandler()


ui.server.apiControl = ApiControl(interface)
thread.start_new_thread(ui.server.app.run())