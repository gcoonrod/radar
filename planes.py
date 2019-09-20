from collections import namedtuple

from color import HSV

PlaneType = namedtuple("PlaneType", "type hsv")

DEFAULT = PlaneType("default", HSV(54, .3, 1.0))
STATIC = PlaneType("static", HSV(3, .99, 1.0))
A38 = PlaneType("A38", HSV(0., .99, 1.0))
B74 = PlaneType("B74", HSV(336, .974, 1.0))
B77 = PlaneType("B77", HSV(227, .99, 1.0))
B78 = PlaneType("B78", HSV(205, .94, 1.0))
B73 = PlaneType("B73", HSV(133, .89, 1.0))
A32 = PlaneType("A32", HSV(284, .12, 1.0))
A31 = PlaneType("A31", HSV(284, .12, 1.0))
A33 = PlaneType("A33", HSV(178, .198, 1.0))
A34 = PlaneType("A34", HSV(126, .96, 1.0))
