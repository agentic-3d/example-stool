# Stool, assembled and upright: seat, two side frames (+Y and -Y), two cross stretchers (along Y). Origin: floor center.
# The parts stay separate bodies with a CLEARANCE gap at every joint. Print them from stool_print.
# Assembly: dry-fit first. Glue both stretchers into one frame (flat down), add the second frame, then push
# all four leg pegs into the seat together. The frames close in by ~0.8 mm per side as they seat, and the
# stretcher pegs slide deeper by the same amount, so do not let the stretcher glue set before the seat is on.
# Expect: bodies=5 (check with `--bodies 5`), bbox 92.6 x 92.6 x 120
from build123d import Compound, Location, Plane, Pos, Rot

from models import stool_frame, stool_seat, stool_stretcher
from models.stool_params import COS, CROSS_X, FOOT_X, HEIGHT, LEG_AXIS_Z, SIN, STRETCHER_BED_Z, TAN

# frame coordinates -> world, +Y frame: the leg axes plane passes through the feet and leans inward by the splay
FRAME_PLANE = Plane(origin=(0, FOOT_X - LEG_AXIS_Z * COS, -LEG_AXIS_Z * SIN), x_dir=(-1, 0, 0), z_dir=(0, 1, TAN))
# stretcher print coordinates -> world: length along Y, bed flat down
STRETCHER_PLANE = Plane(origin=(CROSS_X, 0, STRETCHER_BED_Z), x_dir=(0, 1, 0), z_dir=(0, 0, 1))

seat = Pos(0, 0, HEIGHT) * Rot(180, 0, 0) * stool_seat.result
frame = Location(FRAME_PLANE) * stool_frame.result
stretcher = Location(STRETCHER_PLANE) * stool_stretcher.result

result = Compound([seat, frame, Rot(0, 0, 180) * frame, stretcher, Pos(-2 * CROSS_X, 0, 0) * stretcher])
