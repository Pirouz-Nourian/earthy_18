#__author__ = "Yamuna Sakthivel (4738578)"
#__version__ = "2018.09.14"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math as math

#Bounding box of the brep
bbox = x.GetBoundingBox(True)

#Length, width and height of the bounding box
W = bbox.Diagonal.X
L = bbox.Diagonal.Y
H = bbox.Diagonal.Z

#diving the three axis by the dimension of the voxel

XC = int(math.ceil(W/y))
YC = int(math.ceil(L/z))
ZC = int(math.ceil(H/u))
print (ZC)

points = []
distlist = []

#Base plane
bpoint = bbox.Min
bXV = rg.Vector3d.XAxis
bYV = rg.Vector3d.YAxis

bplane = rg.Plane(bpoint, bXV, bYV)

xshift = y/2
yshift = z/2
zshift = u/2

for i in range (0,XC) :
    for j in range (0,YC) :
        for k in range (0,ZC) :
            point = bplane.PointAt(i*y + xshift, j*z + yshift, k*u + zshift)
            points.append(point)
            cpoint = x.ClosestPoint(point)
            distance = point.DistanceTo(cpoint)
            if (x.IsPointInside(point, 0.1, True)):
                distance = -distance
            else:
                distance = distance
            distlist.append(distance)
print distlist
b = points
c = distlist