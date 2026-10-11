# Stool parameters (mm). No geometry and no `result`: every stool_* model imports this module, so no number is retyped.
#
# Function:   120 mm scale-model stool, glued from 5 printed parts
# Printer:    256^3, BED_MAX 240, no AMS
# Process:    FDM; seat top-face down; frames and stretchers lying on a bed flat
# Parts:      stool_seat x1, stool_frame x2 (identical), stool_stretcher x2 (identical)
# Split:      slab + slender + horizontal members need different orientations;
#             cut where the legs meet the seat and where the Y stretchers meet the legs
# Joints:     leg -> seat: the full leg section is the peg, floor stop, its bed flat lets glue and air out
#             stretcher -> leg: shouldered peg, the shoulder lands on the leg's bed flat, socket GLUE_GAP deeper
#             clearance CLEARANCE (0.2) per side; two pegs per frame key its orientation
# Plates:     stool_print, 5 bodies, no supports
# Datums:     floor plane, X and Y centerlines
# Risks:      seat joint depth is 0.65 x the leg diameter, below the 1 x target (the seat is only 12 thick);
#             the frame sockets open onto the bed, their floor is a 6.4 mm bridge (not a stop face)
#
# Frame coordinates (print orientation of a side frame): X across the frame, Y up the frame from the floor line,
# Z = 0 on the bed. Two adjacent splayed legs are coplanar, and that plane is tilted by SPLAY_DEG from vertical.
from math import asin, cos, degrees, radians, sin, sqrt, tan

from models.common import BED_MAX, CLEARANCE, GLUE_GAP, MIN_WALL, SOCKET_FLOOR, SOCKET_WALL

# --- Given: proportions from the reference photos, as ratios of HEIGHT ---
HEIGHT = 120
SEAT_W_RATIO = 0.70
SEAT_T_RATIO = 0.10
LEG_D_RATIO = 0.115
STRETCHER_D_RATIO = 0.075
STRETCHER_Z_RATIO = 0.32  # stretcher axis height above the floor
SPLAY_DEG = 5  # leg lean per axis
LEG_INSET = 12  # leg axis distance from the seat edge, at the seat underside
SEAT_CORNER_R = 8
SEAT_TOP_CHAMFER = 2  # seat top edge, on the bed when printed
SEAT_BOTTOM_R = 3  # seat underside edge

# --- Assumed: joints and print flats ---
FLAT_DEG = 45  # half-angle of the bed flat on a round member; the overhang beside it is 90 - FLAT_DEG
LEG_JOINT_DEPTH = 9  # leg peg length inside the seat, along the peg
PEG_D = 6  # stretcher peg
PEG_DEPTH = 7  # stretcher peg length from its shoulder
PEG_ROOT = 1  # 45 deg relief at the peg root; the socket mouth is countersunk by the same amount
LEAD_IN = 0.5  # chamfer on peg tips and on the seat socket mouths
FOOT_CHAMFER = 1

# --- Derived ---
SEAT_W = HEIGHT * SEAT_W_RATIO
SEAT_T = HEIGHT * SEAT_T_RATIO
SEAT_Z = HEIGHT - SEAT_T  # seat underside
LEG_D = HEIGHT * LEG_D_RATIO
LEG_R = LEG_D / 2
STRETCHER_R = HEIGHT * STRETCHER_D_RATIO / 2
STRETCHER_Z = HEIGHT * STRETCHER_Z_RATIO
PEG_R = PEG_D / 2

TAN, SIN, COS = tan(radians(SPLAY_DEG)), sin(radians(SPLAY_DEG)), cos(radians(SPLAY_DEG))
SEC = 1 / COS  # frame Y per unit of world Z along a leg axis
LEG_TOP_X = SEAT_W / 2 - LEG_INSET  # leg axis at the seat underside
FOOT_X = LEG_TOP_X + TAN * SEAT_Z  # leg axis at the floor

LEG_SOCKET_R = LEG_R + CLEARANCE
LEG_SOCKET_DEPTH = LEG_JOINT_DEPTH + CLEARANCE  # floor stop: the gap keeps the bodies apart in the model
PEG_SOCKET_R = PEG_R + CLEARANCE
PEG_SOCKET_DEPTH = PEG_DEPTH + GLUE_GAP  # shoulder stop

# bed flats: the axis of a round member sits at r * cos(FLAT_DEG) above the bed
LEG_FLAT_HALF = PEG_SOCKET_R + PEG_ROOT + MIN_WALL  # wide enough to leave a wall beside the countersunk socket mouth
LEG_AXIS_Z = sqrt(LEG_R**2 - LEG_FLAT_HALF**2)
STRETCHER_AXIS_Z = STRETCHER_R * cos(radians(FLAT_DEG))
PEG_AXIS_Z = PEG_R * cos(radians(FLAT_DEG))  # the peg shares the stretcher's bed plane, so it is eccentric

# cross stretchers, world: flat down, axis along Y
STRETCHER_BED_Z = STRETCHER_Z - STRETCHER_AXIS_Z  # world height of the stretcher's bed flat
PEG_Z = STRETCHER_BED_Z + PEG_AXIS_Z  # world height of the peg axis
CROSS_X = FOOT_X - TAN * PEG_Z  # leg axis at the peg height
SHOULDER_Y = FOOT_X - TAN * STRETCHER_BED_Z - SEC * (LEG_AXIS_Z + CLEARANCE)  # shoulder plane at the bed flat

# frame coordinates
RAIL_X = FOOT_X - TAN * STRETCHER_Z  # leg axis at the rail height
FRAME_SEAT_V = SEC * SEAT_Z  # leg axis at the seat underside
FRAME_RAIL_V = SEC * STRETCHER_Z
FRAME_SOCKET_V = SEC * PEG_Z + TAN * LEG_AXIS_Z  # stretcher socket mouth on the bed face
FRAME_W = 2 * (FOOT_X + LEG_R * SEC)  # bbox estimate
FRAME_H = FRAME_SEAT_V + LEG_JOINT_DEPTH + LEG_R * TAN

# --- Rule checks (RULES.md steps 4 and 7) ---
assert LEG_JOINT_DEPTH >= 0.5 * LEG_D and PEG_D >= 5 and PEG_DEPTH >= PEG_D  # joint depth
assert SEAT_T - (LEG_SOCKET_DEPTH * COS + LEG_SOCKET_R * SIN) >= SOCKET_FLOOR  # floor above the leg socket
assert LEG_INSET - LEG_SOCKET_R - LEAD_IN >= max(SOCKET_WALL, SEAT_BOTTOM_R)  # wall, and clear of the underside fillet
assert LEG_R - PEG_SOCKET_R >= SOCKET_WALL  # wall beside the stretcher socket
assert LEG_AXIS_Z + sqrt(LEG_R**2 - PEG_SOCKET_R**2) - (PEG_SOCKET_DEPTH * COS + PEG_SOCKET_R * SIN) >= SOCKET_FLOOR
assert degrees(asin(LEG_FLAT_HALF / LEG_R)) >= FLAT_DEG  # overhang beside the leg flat <= 90 - FLAT_DEG
assert STRETCHER_AXIS_Z - PEG_AXIS_Z + PEG_R < STRETCHER_R  # the peg stays inside the stretcher's end face
assert LEG_AXIS_Z - STRETCHER_AXIS_Z + STRETCHER_R < LEG_R  # the rail ends are buried in the legs
assert max(SEAT_W, FRAME_W, FRAME_H) <= BED_MAX
