# Shared socket cutter for the stool joints. No `result`: subtract it from the host part.
from build123d import Align, Cone, Cylinder, Pos

EXT = 2  # cutter length outside the mouth, so a tilted mouth is cut through cleanly
ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


def socket(r, depth, mouth):
    """Bore along +Z from the mouth at Z = 0, with a 45 deg countersink of `mouth` (lead-in, clears the peg root)."""
    bore = Cylinder(r, depth + EXT, align=ALIGN) + Cone(r + mouth + EXT, r, mouth + EXT, align=ALIGN)
    return Pos(0, 0, -EXT) * bore
