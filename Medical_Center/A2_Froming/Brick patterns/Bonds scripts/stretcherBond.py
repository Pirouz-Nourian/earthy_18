"""Stretcher bond."""

__author__ = "nchristidi"
__version__ = "2018.10.07"

import Rhino.Geometry as rg

class brickWall:
    def __init__ (self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.orPt = rg.Point3d(0, width,0)
        self.peakPt = rg.Point3d(0, width, height)
    def createWall (self):
        basePlane = rg.Plane.WorldXY
        xSize = rg.Interval(0, self.length)
        ySize = rg.Interval(0, self.width)
        zSize = rg.Interval(0, self.height)
        wall = rg.Box(basePlane, xSize, ySize, zSize)
        wall = wall.ToBrep()
        return wall

class brick:
    def __init__ (self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
    def stretcher (self, orPt):
        basePlane = rg.Plane.WorldXY
        xSize = rg.Interval(orPt[0], orPt[0]+self.length)
        ySize = rg.Interval(orPt[1], orPt[1]-self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        return brick
    def halfBrick (self, orPt):
        basePlane = rg.Plane.WorldXY
        xSize = rg.Interval(orPt[0], orPt[0]+self.length/2)
        ySize = rg.Interval(orPt[1], orPt[1]-self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        return brick

bw = brickWall(length, width, height)
b = brick(brLength, brWidth, brHeight)
wall = bw.createWall()
faces = wall.Faces
face = faces.ExtractFace(2)
contours = rg.Brep.CreateContourCurves(face, bw.orPt, bw.peakPt, brHeight)
bricks = []
counter = 0
for contour in contours:
    contour.Reverse()
    contour.Domain = rg.Interval(0,1)
    t = contour.DivideByLength(brLength/2, True)
    listL= len(t)
    for i in range(len(t)-1):
        pt = contour.PointAt(t[i])
        if counter%2==0:
            if i==0:
                bricks.append(b.halfBrick(pt))
            elif i%2==1:
                bricks.append(b.stretcher(pt))
        else:
            if i%2==0:
                bricks.append(b.stretcher(pt))
    pt = contour.PointAt(t[len(t)-1])
    if listL%2==0:
        if counter%2==0:
            bricks.append(b.halfBrick(pt))
    else:
        if counter%2==1:
            bricks.append(b.halfBrick(pt))
    counter +=1

a = bricks