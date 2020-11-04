import rhinoscriptsyntax as rs
import math as math
import Rhino.Geometry as rg

#Points controlling the extent of the contour curves
pt1 = rg.Point3d(0,0,0)
pt2 = rg.Point3d(0,0,15)
#srf to Brep
srf = wall.ToBrep()

#Creating empty list so points are added after the loop
contourpts=[]
bricks = []

#Contours curves of the surface with interval = bricks height
contour = srf.CreateContourCurves(srf,pt1,pt2,brickH)
#Returns = List of curves

#Pythogaros theorem which defines the distance between the curve/splitting distance.Used to get additionallength and avoid overlap.
dia = math.sqrt(brickL**2+brickH**2)
#Loop1: Splitting the curves into points - based on Pythogaros theorem
for i in contour:
    divide = rs.DivideCurveLength(i,dia,True,True)

#Loop2: Analyzing the splitted point and getting parameters(plane) - origin,orientation -

    for pts in divide:
#Takes the curve and point and returns a point with parameter which is the input for FrameAt(orienting_itself)
        close_pt = rs.CurveClosestPoint(i,pts)
        (bool, pln) = i.FrameAt(close_pt)
        contourpts.append(pln)
#Returns = A list of plane at the divided points, with correct orientation

#Size of Brick - Input
        x = rg.Interval(0,brickL)
        y = rg.Interval(0,brickW)
        z = rg.Interval(0,brickH)

#Creating brick with the existing plane data and inputs
        brick = rg.Box(pln,x,y,z)
        bricks.append(brick)
#Bricks automatically created at the point with the orientation similar to ths surface

print(bricks)
