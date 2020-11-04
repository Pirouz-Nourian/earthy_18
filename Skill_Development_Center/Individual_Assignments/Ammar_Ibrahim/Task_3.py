import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax
import math as math

#get bounding box for cone

bbox= cone.GetBoundingBox(True)
W= bbox.Diagonal.X
L= bbox.Diagonal.Y
H= bbox.Diagonal.Z
#XC is count of boxes 
points=[]
dist=[]

XC=int(math.ceil(W/xs))
YC=int(math.ceil(L/ys))
ZC=int(math.ceil(H/zs))

xshift = xs/2
yshift =ys/2
zshift =zs/2

bPoint= bbox.Min
bXV= rg.Vector3d.XAxis
bYV= rg.Vector3d.YAxis

bPlane= rg.Plane(bPoint, bXV, bYV)

for i in range(0,XC):
    for j in range(0,YC):
        for k in range(0,ZC):
            point= bPlane.PointAt(i*xs+xshift,j*ys+yshift,k*zs+zshift)
            points.append(point)
            cpoint= cone.ClosestPoint(point)
            distance= point.DistanceTo(cpoint)
            if (cone.IsPointInside(point,0.1,True)):
                distance= -distance
            else:
                distance= distance
            dist.append(distance)
            
b= points
c= dist

print(dist)