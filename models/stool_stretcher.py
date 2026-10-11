# Stool cross stretcher in print orientation: round rod along X lying on its bed flat (Z = 0). Origin: bottom center.
# It joins the two side frames. The shoulders are cut parallel to the leg flats (tilted by the splay,
# wider at the bed, so no overhang). The pegs share the bed plane, which makes them eccentric and
# gives them their own flat for glue and air. The peg root has a 45 deg relief, clipped to the rod section.
# Glue it with the flat facing the floor.
# Expect: bodies=1, bbox 77.3 x 9 x 7.7
from build123d import Align, Cone, Cylinder, Keep, Plane, Pos, Rot, mirror, split

from models.stool_params import LEAD_IN, PEG_AXIS_Z, PEG_DEPTH, PEG_R, PEG_ROOT, SHOULDER_Y, STRETCHER_AXIS_Z, STRETCHER_R, TAN

BACK = 1  # peg overlap into the rod, behind the tilted shoulder
ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


def build(shoulder_x=SHOULDER_Y, r=STRETCHER_R, axis_z=STRETCHER_AXIS_Z, peg_r=PEG_R, peg_axis_z=PEG_AXIS_Z, peg_l=PEG_DEPTH, root=PEG_ROOT, lead_in=LEAD_IN, splay_tan=TAN):
    envelope = Pos(0, 0, axis_z) * Cylinder(r, 2 * (shoulder_x + peg_l + BACK), rotation=(0, 90, 0))
    rod = envelope
    for sx in (1, -1):
        rod = split(rod, bisect_by=Plane(origin=(sx * shoulder_x, 0, 0), z_dir=(sx, 0, splay_tan)), keep=Keep.BOTTOM)
    peg = Cylinder(peg_r, BACK + peg_l - lead_in, align=ALIGN) + Pos(0, 0, BACK + peg_l - lead_in) * Cone(peg_r, peg_r - lead_in, lead_in, align=ALIGN) + Cone(peg_r + root + BACK, peg_r, root + BACK, align=ALIGN)
    peg = Pos(shoulder_x - splay_tan * peg_axis_z - BACK, 0, peg_axis_z) * Rot(0, 90, 0) * peg  # starts BACK behind the shoulder
    pegs = (peg + mirror(peg, Plane.YZ)) & envelope
    return split(rod + pegs, bisect_by=Plane.XY, keep=Keep.TOP)  # bed flat


result = build()
