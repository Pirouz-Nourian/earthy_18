"""
The script places bricks in a dome-surface. Suggestions for future work include the alternating 
pattern for the bricks. 
    Inputs:
        srf: The surface of the dome (surface).
        horCrvs: Horizontal curves on the surface, with same distance between them (list of curves).
        brick: The Brep of the brick to be used (Brep).
        brk_ht: The height of the brick (float).
        brk_len: The length of the brick (float).
        y_spacing: The space between the bricks in y-axis(float).
        x_spacing: The space between the bricks in x-axis(float).
    Output:
        a: Bricks (list).
"""
__author__ = "Despoina Pouniou, Erron Estrado"
__version__ = "2018.10.17"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Collections as rc
import math
from copy import copy


#Get center point on brick.
b_area = rg.AreaMassProperties.Compute(brick)
brick_center = b_area.Centroid
surface = brick.Faces[5]
closestpt = surface.ClosestPoint(brick_center)
normal = surface.NormalAt(closestpt[1], closestpt[2])
brk = brick

bricks = []
#Start placement loops.
for crv in horCrvs:
    #If curve is shorter than brick length then skip
    if crv.GetLength() <= brk_len:
        continue
    #Divide curve by brick length.
    t = crv.DivideByLength(brk_len, True)
    #Rotate and move brick into position.
    for i, item in enumerate(t):
        dest_pt = crv.PointAt(item)
        dir = dest_pt - brick_center
        tangvec = crv.TangentAt(item)
        pt = srf.ClosestPoint(dest_pt)
        norm = srf.NormalAt(pt[1], pt[2])
        norm.Reverse()
        new_brick = copy(brk)
#------------------------------------------------------------------
        plane0=rg.Plane(brick_center, normal)
        plane05=rg.Plane(brick_center,plane0.YAxis, plane0.XAxis)
        plane1=rg.Plane(dest_pt, norm, tangvec)
#------------------------------------------------------------------
        transform= rg.Transform.PlaneToPlane(plane05, plane1)
        new_brick.Transform(transform)
        bricks.append(new_brick)

a = bricks
