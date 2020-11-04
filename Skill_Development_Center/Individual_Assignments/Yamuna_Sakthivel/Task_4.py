"""Possible future updates:
    Add different brick bond functions. Maybe a system as per Koen his presentation of 2018-09-04"""

#__author__ = "Yamuna Sakthivel (4738578)"
#__version__ = "2018.09.14"

#Possible improvents in the future
    #The bricks can be arranged without overlapping
    #The extra bricks at the curve ends should me made half bricks

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math as math

#Creating the bounding box of the Input brep

bbox = B.GetBoundingBox(True)
Min = bbox.Min[2]
Max = bbox.Max[2]
pointa = rg.Point3d(0,0,Min)
pointb = rg.Point3d(0,0,Max)
interval = 0.092

#divide the brep into contours
#get the list of the contours
#divide the contour lines into (curve_length/x)

#Creating contours on the brep
contours = B.CreateContourCurves(B,pointa,pointb, interval)
b = contours
contours = []
pointlist = []
frames = []
brick_all = []

#Dividing the contours into segments (curve_length/x) and extracting the points as reference for placing the bricks
for i in b:
    points = rs.DivideCurveLength(i, x * 1.2, True)
    for pts in points:
        pointlist.append(pts)
        tlist = rs.CurveClosestPoint(i,pts)
        (bool, frameat) = i.FrameAt(tlist)
        frames.append(frameat)

#The correction factor 1.2 in line 38 should be made into an genneral expression such that its applicable in any case.
#Defining the size of the brick (x,y,z) as mentioned in the slider input of grasshopper

Length = rg.Interval(0,x)
Width = rg.Interval (0,y)
Height = rg.Interval (0,z)

#Formulating bricks at every point on the contours

for j in frames:
    brick = rg.Box(j,Length, Width, Height)
    brick_all.append(brick)

a = pointlist
c = brick_all

#To ensure that the bricks dont intersect with each other, the legth of the divisions my be take taken as the diagonals length
    #diagonal_length = math.ceil((i.GetLength())/(((Width) ** 2 + (Length) ** 2)** 0.5)
