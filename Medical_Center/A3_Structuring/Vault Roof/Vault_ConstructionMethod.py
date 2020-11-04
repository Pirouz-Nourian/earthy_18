"""Provides a scripting component.
    Inputs:
        isoCrvs: Isocurves from surface
    Output:
        line1: Hypotenuse
        line2: Vertical
        length1: Length of hypotenuse
        length2: Length of vertical
        points: Point at row"""

__author__ = "erron"
__version__ = "2018.10.18"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Collections as rc
from copy import copy
import math

# initialise variables and lists
workingCrvs = isoCrvs
endPts = []
lines1 = []
lines2 = []
distances1 = []
distances2 = []
nums = []
plinePts = []

# get list of end points
for crv in isoCrvs:
    endPts.append(crv.PointAtStart)

# get arch base point
pt1 = endPts[0]
pt2 = endPts[endPts.Count-1]
basePt = (pt1 + pt2)/2

# determine range depending if even or odd number of curves
if endPts.Count%2 == 0:
    ptRange = int(endPts.Count/2)
else:
    ptRange = int(endPts.Count/2) + 1

# get distances
for i in range(0, ptRange):
    # length 1
    lines1.append(rg.LineCurve(basePt, endPts[i]))
    dist1 = basePt.DistanceTo(endPts[i])
    dist1 = float("{0:.3f}".format(dist1))
    distances1.append(dist1)
    
    # length 2
    vertPt = copy(endPts[i])
    vertPt.Z = basePt.Z
    lines2.append(rg.LineCurve(endPts[i], vertPt))
    dist2 = vertPt.DistanceTo(endPts[i])
    dist2 = float("{0:.3f}".format(dist2))
    distances2.append(dist2)

# return half the points
sliceObj = slice(ptRange)
Pts = endPts[sliceObj]

# outputs
line1 = lines1
line2 = lines2
length1 = distances1
length2 = distances2
points = Pts