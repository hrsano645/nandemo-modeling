import numpy as np
import cadquery as cq
from svgpathtools import svg2paths, Line, CubicBezier
from ocp_vscode import show_object
from pathlib import Path

s = cq.Workplane("XY")
sPnts = [
    (2.75, 1.5),
    (2.5, 1.75),
    (2.0, 1.5),
    (1.5, 1.0),
    (1.0, 1.25),
    (0.5, 1.0),
    (0, 1.0),
]
r = s.lineTo(3.0, 0).lineTo(3.0, 1.0).spline(sPnts, includeCurrent=True).close()
result = r.extrude(0.5)

show_object(result)

# # Workplaneの定義
# result = cq.Workplane("XY")

# # ベースプレートを書いていく
# result = (
#     result.moveTo(0, 5)
#     .threePointArc((40, 0), (80, 5))
#     .lineTo(75, 105)
#     .threePointArc((40, 110), (5, 105))
#     .lineTo(0, 5)
#     .close()
# )

# show_object(result)
