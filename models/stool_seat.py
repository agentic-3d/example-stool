# Stool seat in print orientation: top face on the bed (Z = 0), underside up. Origin: bottom center.
# The four leg sockets open upward and lean SPLAY_DEG from Z, toward the center along Y (the frame plane).
# The bed edge is a 45 deg chamfer, the underside edge a fillet. Edge details come before the sockets,
# so the edge selectors never see the socket mouths.
# Expect: bodies=1, bbox 84 x 84 x 12
from build123d import Align, Axis, BuildPart, Box, Location, Plane, chamfer, fillet

from models.stool_joint import socket
from models.stool_params import LEAD_IN, LEG_SOCKET_DEPTH, LEG_SOCKET_R, LEG_TOP_X, SEAT_BOTTOM_R, SEAT_CORNER_R, SEAT_T, SEAT_TOP_CHAMFER, SEAT_W, TAN


def build(width=SEAT_W, thickness=SEAT_T, corner_r=SEAT_CORNER_R, top_chamfer=SEAT_TOP_CHAMFER, bottom_r=SEAT_BOTTOM_R, socket_x=LEG_TOP_X, socket_r=LEG_SOCKET_R, socket_depth=LEG_SOCKET_DEPTH, splay_tan=TAN, mouth=LEAD_IN):
    with BuildPart() as part:
        Box(width, width, thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(part.edges().filter_by(Axis.Z), corner_r)
        chamfer((part.faces() << Axis.Z).edges(), top_chamfer)
        fillet((part.faces() >> Axis.Z).edges(), bottom_r)
    seat = part.part
    for sx in (1, -1):
        for sy in (1, -1):
            seat -= Location(Plane(origin=(sx * socket_x, sy * socket_x, thickness), z_dir=(0, -sy * splay_tan, -1))) * socket(socket_r, socket_depth, mouth)
    return seat


result = build()
