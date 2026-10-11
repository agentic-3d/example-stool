# Print plate: every stool part in print orientation at Z = 0. No supports. Origin: bottom center.
# Row 1 holds the two frames, row 2 the seat and the two stretchers. The layout is explicit because
# pack() lines these parts up in one 279 mm row, which is over BED_MAX.
# Expect: bodies=5 (check with `--bodies 5`), bbox 190.2 x 206.9 x 12
from build123d import Compound, Pos

from models import stool_frame, stool_seat, stool_stretcher
from models.common import BED_MAX

PADDING = 5  # gap between parts on the bed


def at(part, x, y):
    """Move the part so the min corner of its bbox sits at (x, y, 0)."""
    lo = part.bounding_box().min
    return Pos(x - lo.X, y - lo.Y, -lo.Z) * part


seat, frame, stretcher = stool_seat.result, stool_frame.result, stool_stretcher.result
frame_size, seat_size, stretcher_size = frame.bounding_box().size, seat.bounding_box().size, stretcher.bounding_box().size
row2 = frame_size.Y + PADDING
col2 = seat_size.X + PADDING

plate = Compound([at(frame, 0, 0), at(frame, frame_size.X + PADDING, 0), at(seat, 0, row2), at(stretcher, col2, row2), at(stretcher, col2, row2 + stretcher_size.Y + PADDING)])
size = plate.bounding_box().size
assert max(size.X, size.Y) <= BED_MAX

result = Pos(-size.X / 2, -size.Y / 2, 0) * plate
