import Rhino.Geometry as rg
import math as math
import rhinoscriptsyntax as rs

Bbox =S.GetBoundingBox(True)
W = Bbox.Diagonal.X
L = Bbox.Diagonal.Y
H = Bbox.Diagonal.Z
#print(W)
XC = int(math.ceil(W/xS))
YC = int(math.ceil(L/yS))
ZC = int(math.ceil(H/zS))

points = []
distList = []
print(Bbox)
bPoint = Bbox.Min
print(bPoint)
bXV = rg.Vector3d.XAxis
bYV = rg.Vector3d.YAxis

xShift = xS/2
yShift = yS/2
zShift = zS/2

bplane=rg.Plane(bPoint, bXV, bYV)

for i in range(0,XC):
    for j in range(0,YC):
        for k in range(0,ZC):
            point = bplane.PointAt(i*xS+xShift,j*yS+yShift,k*zS+zShift)
            points.append(point)
            cPoint = S.ClosestPoint(point)
            distance = point.DistanceTo(cPoint)
            if(S.IsPointInside(point, 0.1, True)):
                distance = -distance
            else:
                distance = distance
            distList.append(distance)
#print(distList)
b = points
c = distList