import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino 
import math as math
import scriptcontext as sc

#inputs // brick dimensions // wall surface

brickL=length
brickW=width
brickH=height

srf=surface

#bounding box for srf

Bbox=surface.GetBoundingBox(True)
H = Bbox.Diagonal.Z
H=int(H)

#contours

crv = rs.AddSrfContourCrvs(srf,([0,0,0], [0,0,H]), interval=brickH)
contours=crv

#divide contours into segments

points=[]
pointsAll=[]

for i in range(len(contours)) :
    points= rs.DivideCurveLength(contours[i],brickL,True,True)
    pointsAll.extend(points)

#bricks

    placedBricks=[]
    b=[]
    j=1
    for j in range(len(pointsAll)-2):
        x=[]
        y=[]
        z=[]
        rectangle=[]
        curve=[]
        plane=rg.Plane(pointsAll[j],rs.VectorCreate(pointsAll[j-1],pointsAll[j]),rg.Vector3d(0,0,1))
        x=pointsAll[j].X
        y=pointsAll[j].Y
        z=pointsAll[j].Z
        rectangle = rg.Rectangle3d(plane, brickL,brickW)
        rectangleCrv=rg.Rectangle3d.ToNurbsCurve(rectangle)
        curve = rs.AddLine((x+brickL,y,z), (x+brickL,y,z+brickH))
        placedBrick=rg.Extrusion.Create(rectangleCrv,brickH,True)
        placedBricks.append(placedBrick)
b=placedBricks

