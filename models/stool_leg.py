# Stool leg: component of stool_frame (not printed alone), lying on its bed flat in frame coordinates.
# This is the +X leg. Its axis leans toward the frame center going up. The foot and the top are cut
# parallel to the floor, which is tilted by the splay in frame coordinates. Above the seat underside
# the leg continues as the peg, straight up the frame (+Y), so both pegs of a frame are parallel.
# Expect: bodies=1, bbox 23.2 x 117.9 x 11.2
from math import sqrt

from build123d import Align, Axis, Cone, Cylinder, Keep, Location, Plane, Pos, Rot, Vector, chamfer, split

from models.stool_params import FOOT_CHAMFER, FOOT_X, FRAME_SEAT_V, LEAD_IN, LEG_AXIS_Z, LEG_JOINT_DEPTH, LEG_R, SEC, TAN

EXTRA = 5  # rod and peg overlength, removed by the floor and seat cuts
ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


def build(foot_x=FOOT_X, seat_v=FRAME_SEAT_V, r=LEG_R, axis_z=LEG_AXIS_Z, peg_l=LEG_JOINT_DEPTH, splay_tan=TAN, foot_chamfer=FOOT_CHAMFER, lead_in=LEAD_IN):
    rise = seat_v / SEC  # world height of the seat underside
    foot, top = Vector(foot_x, 0, axis_z), Vector(foot_x - splay_tan * rise, seat_v, axis_z)
    level = (0, 1, splay_tan)  # world Z in frame coordinates
    rod = Location(Plane(origin=foot, z_dir=top - foot)) * Pos(0, 0, -EXTRA) * Cylinder(r, rise * sqrt(1 + 2 * splay_tan**2) + 2 * EXTRA, align=ALIGN)
    rod = split(rod, bisect_by=Plane(origin=foot, z_dir=level), keep=Keep.TOP)
    rod = split(rod, bisect_by=Plane(origin=top, z_dir=level), keep=Keep.BOTTOM)
    peg = Cylinder(r, EXTRA + peg_l - lead_in, align=ALIGN) + Pos(0, 0, EXTRA + peg_l - lead_in) * Cone(r, r - lead_in, lead_in, align=ALIGN)
    peg = split(Pos(top) * Rot(-90, 0, 0) * Pos(0, 0, -EXTRA) * peg, bisect_by=Plane(origin=top, z_dir=level), keep=Keep.TOP)
    leg = split(rod + peg, bisect_by=Plane.XY, keep=Keep.TOP)  # bed flat
    return chamfer(leg.faces().sort_by(Axis.Y)[0].edges(), foot_chamfer)


result = build()
