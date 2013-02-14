import UI.server
import thread
from UI.api import ApiControl
from UI.simulator import Simulator
interface = Simulator()
UI.server.apiControl = ApiControl(interface)
thread.start_new_thread(UI.server.app.run())