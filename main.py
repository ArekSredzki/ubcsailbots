import ui.server
import thread
from ui.api import ApiControl
from ui.simulator import Simulator
interface = Simulator()
ui.server.apiControl = ApiControl(interface)
thread.start_new_thread(ui.server.app.run())