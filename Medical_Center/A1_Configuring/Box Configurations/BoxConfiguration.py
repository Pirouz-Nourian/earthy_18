"""Creates a building module.
    Inputs:
        Name: Name of Room
        module_x: Size of 1 module in x
        module_y: Size of 1 module in y
        mods_x: number of modules in x direction
        mods_y: number of modules in y direction
    Output:
        box: Room box
        area: Area of room
        pts: attachment points"""

__author__ = "erron estrado"
__version__ = "2018.09.21"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
from copy import copy

# create box points
def ConstructBoxPts(module_x, module_y, mods_x, mods_y, ins_pt):
    anchorPts = []
    anchorPts.append(ins_pt)
    prev_pt = ins_pt
    
    # make points of first edge
    for i in range(mods_x):
        pt = copy(prev_pt)
        vector = rg.Vector3d.XAxis * module_x * (i+1)
        pt += vector
        anchorPts.append(pt)
        pt = prev_pt
    prev_pt = anchorPts[anchorPts.Count - 1]
    
    # make points of second edge
    for i in range(mods_y):
        pt = copy(prev_pt)
        vector = rg.Vector3d.YAxis * module_y * (i+1)
        pt += vector
        anchorPts.append(pt)
        pt = prev_pt
    prev_pt = anchorPts[anchorPts.Count - 1]
    
    # make points of third edge
    for i in range(mods_x):
        pt = copy(prev_pt)
        vector = rg.Vector3d.XAxis * module_x * (i+1) * -1
        pt += vector
        anchorPts.append(pt)
        pt = prev_pt
    prev_pt = anchorPts[anchorPts.Count - 1]
    
    # make points of fourth edge
    for i in range(mods_y):
        pt = copy(prev_pt)
        vector = rg.Vector3d.YAxis * module_y * (i+1) *-1
        pt += vector
        anchorPts.append(pt)
        pt = prev_pt
    
    # make box curve
    
    return anchorPts

# snapping to other boxes
def Snap(snapPts, boxPts):
    if snapPts.Count != 0:
        closestPts = []
        dist = boxPts[0].DistanceTo(snapPts[0])
        for pt in boxPts:
            for pt2 in snapPts:
                distToPt = pt.DistanceTo(pt2)
                if distToPt < dist:
                    dist = distToPt
                    closestPts.Clear()
                    closestPts.append(pt)
                    closestPts.append(pt2)
        vec = closestPts[1] - closestPts[0]
        
        # new moved anchor points
        newAnchors = []
        for pt in boxPts:
            pt += vec
            newAnchors.append(pt)
    else:
        newAnchors = boxPts
    return newAnchors

def DrawBox(points):
    polycurve = rg.PolylineCurve(points)
    return polycurve

# get interior lines of individual modules
def GetGridLines(module_x, module_y, mods_x, mods_y, ins_pt):
    modules = []
    start_pt = ins_pt
    for i in range(mods_y+1):
        for j in range(mods_x):
            plane = rg.Plane(start_pt, rg.Vector3d.ZAxis)
            mod = rg.Rectangle3d(plane, module_x, module_y)
            modules.append(mod)
            vec_x = rg.Vector3d.XAxis * module_x
            start_pt += vec_x
        start_pt = ins_pt
        start_pt += rg.Vector3d.YAxis * module_y * i
    return modules

# run functions
roomPts = ConstructBoxPts(module_x, module_y, mods_x, mods_y, ins_pt)
newPts = Snap(attach_pts, roomPts)
room = DrawBox(newPts)

# get area properties
roomProperties = rg.AreaMassProperties.Compute(room)

# outputs
grid = GetGridLines(module_x, module_y, mods_x, mods_y, newPts[0])
centroid = roomProperties.Centroid
area = roomProperties.Area
tag = '{}\n{}m2'.format(name, area)
box = room
pts = newPts