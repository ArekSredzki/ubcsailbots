'''
Created on Jan 26, 2013

Static Variables for the control logic and GUI
-   All static variables are contained within the StaticVars module.
    If you wish to add a new challenge, you must define its name 
    inside of StaticVars.  Any new Waypoint types must also be added 
    to StaticVars.

'''

# Constant names for challenges and logic
NAVIGATION_CHALLENGE = "navigation"
STATION_KEEPING_CHALLENGE = "stationkeeping"
LONG_DISTANCE_CHALLENGE = "longdistance"
NO_CHALLENGE = "NONE"
CHASE_RACE_CHALLENGE = "chaserace"

# -- Logic Waypoint Types --
# Point to Point waypoint types
GO_TO = "pointToPoint"

# Round Buoy waypoint types
GO_AROUND = "roundbuoy"

# -- Challenge Waypoint types --
# Long Distance Challenge waypoint types
LD_START_FINISH = "ld_start_finish"
LD_FIRST = "ld_first"
LD_SECOND = "ld_second"

# Navigation Challenge waypoint types
NAV_FIRST = "nav_first"
NAV_START_PORT ="nav_start_port"
NAV_START_STARBOARD ="nav_start_stbd"

# Station Keeping Challenge waypoint types
SK_TOP_LEFT = "sk_top_left"
SK_TOP_RIGHT = "sk_top_right"
SK_BOTTOM_LEFT = "sk_bottom_left"
SK_BOTTOM_RIGHT = "sk_bottom_right"

# Thresholds for sailing logic functions
AWA_THRESHOLD = 0.9         #Since the table has non-realistic values for AWA, this allows the AWA lookup to be off slightly
SOG_THRESHOLD = 0.9
SPEED_AFFECTION_THRESHOLD = 30     #Speed threshold at which lower speeds are shown to note have a significant variation between AWA and TWA

