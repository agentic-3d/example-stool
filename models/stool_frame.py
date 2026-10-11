# Stool side frame in print orientation: two legs and the rail between them, lying on their bed flats (Z = 0).
# The flat is the inward face of the frame, hidden in the assembled stool. X across the frame, Y from the
# floor line up to the pegs. The rail is shifted toward the bed so its flat is coplanar with the leg flats.
# The two stretcher sockets open onto the bed face and lean SPLAY_DEG from Z (world Y). Print two.
# Expect: bodies=1, bbox 92.6 x 117.9 x 11.2
from build123d import Cylinder, Keep, Location, Plane, Pos, mirror, split

from models import stool_leg
from models.stool_joint import socket
from models.stool_params import CROSS_X, FRAME_RAIL_V, FRAME_SOCKET_V, PEG_ROOT, PEG_SOCKET_DEPTH, PEG_SOCKET_R, RAIL_X, STRETCHER_AXIS_Z, STRETCHER_R, TAN


def build(rail_x=RAIL_X, rail_v=FRAME_RAIL_V, rail_r=STRETCHER_R, rail_axis_z=STRETCHER_AXIS_Z, socket_x=CROSS_X, socket_v=FRAME_SOCKET_V, socket_r=PEG_SOCKET_R, socket_depth=PEG_SOCKET_DEPTH, mouth=PEG_ROOT, splay_tan=TAN):
    leg = stool_leg.build()
    rail = Pos(0, rail_v, rail_axis_z) * Cylinder(rail_r, 2 * rail_x, rotation=(0, 90, 0))
    frame = split(leg + mirror(leg, Plane.YZ) + rail, bisect_by=Plane.XY, keep=Keep.TOP)  # bed flat of the rail
    for sx in (1, -1):
        frame -= Location(Plane(origin=(sx * socket_x, socket_v, 0), z_dir=(0, -splay_tan, 1))) * socket(socket_r, socket_depth, mouth)
    return frame


result = build()
