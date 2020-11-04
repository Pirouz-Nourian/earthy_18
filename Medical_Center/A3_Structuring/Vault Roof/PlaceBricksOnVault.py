"""Provides a scripting component.
    Inputs:
        srf: Surface of vault
        brk_ht: Height of brick
        brk_len: Length of brick
        brk_width: Width of brick
        x_spacing: Horizontal space between bricks
        y_spacing: Vertical space between bricks
    Output:
        brick_out: brick BRep output
        curves: Isocurves at brick rows"""

__author__ = "erron estrado"
__version__ = "2018.10.02"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Collections as rc
import math
from copy import copy

def CreateBrick(length, width, height):
    lenInterval = rg.Interval(0, length)
    widthInterval = rg.Interval(0, width)
    heightInterval = rg.Interval(0, height)
    
    box = rg.Box(rg.Plane.WorldXY, lenInterval, widthInterval, heightInterval)
    brk = box.ToBrep()
    return brk

brick = CreateBrick(brk_len, brk_width, brk_ht)

#set domain equal to length
workSrf = srf
testCrv = workSrf.IsoCurve(1, 0.5)
len = testCrv.GetLength()
workSrf.SetDomain(0, rg.Interval(0,len))

#Create curves for placement of bricks
max = workSrf.Domain(0).Max
i = brk_ht/2
isoCrvs = []

while(i < max):
    crv = workSrf.IsoCurve(0, i)
    isoCrvs.append(crv)
    i += brk_ht + y_spacing

# Get center point on brick
b_vol = rg.VolumeMassProperties.Compute(brick)
brick_center = b_vol.Centroid

# Create half brick(half_brk) and full brick(brk)
scale_x = (0.5 * brk_len) / (brk_len + x_spacing)
scale = rg.Transform.Scale(rg.Plane.WorldXY, scale_x, 1, 1)
half_brk = copy(brick)
half_brk.Transform(scale)
brk = brick

# Initialise lists and extension variable
points = []
bricks = []
ext = 0
brk_len += x_spacing

# Start placement loops
for crv in isoCrvs:
    # if curve is shorter than brick length then skip
    if crv.GetLength() <= brk_len:
        continue
    
    # if ext == 1 extend curve by halfbrick length and set first brick to half_brk
    # to create offset pattern and set ext back to 0
    # else set ext = 1 for next iteration
    if ext == 1:
        crv = crv.Extend(rg.CurveEnd.Start, brk_len/2, rg.CurveExtensionStyle.Line)
        crv = crv.Extend(rg.CurveEnd.End, brk_len/2, rg.CurveExtensionStyle.Line)
        brk = half_brk
        ext = 0
    else:
        ext = 1
    
    # divide curve by brick length
    t = crv.DivideByLength(brk_len, True)
   
    # rotate and move brick into position
    # set brk back to full brick for remainder of points on curve
    for i, item in enumerate(t):
        dest_pt = crv.PointAt(item)
        dir = dest_pt - brick_center
        if i == t.Count - 1 and ext == 0:
            new_brick = copy(half_brk)
            new_brick.Translate(brk_len/2, 0, 0)
        else:
            new_brick = copy(brk)
        # find surface normal at destination point
        pt = workSrf.ClosestPoint(dest_pt)
        norm = workSrf.NormalAt(pt[1], pt[2])
        norm.Reverse()
        # rotate brick to surface normal
        angle = rg.Vector3d.VectorAngle(rg.Vector3d.YAxis, norm, rg.Plane.WorldYZ)
        new_brick.Rotate(angle, rg.Vector3d.XAxis, brick_center)
        # move brick to destination
        new_brick.Translate(dir)
        #add to list
        bricks.append(new_brick)
        brk = brick


brick_out = bricks
curves = isoCrvs
