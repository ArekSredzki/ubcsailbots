import server
import thread
from ui.api import ApiControl
from ui.simulator import Simulator
interface = Simulator()
server.apiControl = ApiControl(interface)
thread.start_new_thread(server.app.run())