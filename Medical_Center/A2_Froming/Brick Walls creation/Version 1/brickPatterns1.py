"""Creates a brick wall.
    Inputs:
        wall: The base wall as a surface (GeometryBase).
        brLength: The brick length (float).
        brWidth: The brick width (float).
        brHeight: The brick height (float).
        curves: The openings as closed curves (Curve).
    Output:
        brickList: The list of bricks."""

__author__ = "nchristidi"
__version__ = "2018.10.07"

import Rhino.Geometry as rg
import math

#Brick class definition
class brick:
    def __init__ (self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
    def custom (self, orPt, dir, header, cLength, cWidth, cHeight):
        basePlane = rg.Plane.WorldXY
        if dir>0:
            xSize = rg.Interval(orPt[0], orPt[0]+cLength)
        else:
            xSize = rg.Interval(orPt[0]-cLength, orPt[0])
        ySize = rg.Interval(orPt[1], orPt[1]+cWidth)
        zSize = rg.Interval(orPt[2], orPt[2]+cHeight)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, rg.Vector3d.ZAxis, orPt)
            brick.Transform(rot)
        return brick
    def strek (self, orPt, dir, header):
        basePlane = rg.Plane.WorldXY
        if dir>0:
            xSize = rg.Interval(orPt[0], orPt[0]+self.length)
        else:
            xSize = rg.Interval(orPt[0]-self.length, orPt[0])
        ySize = rg.Interval(orPt[1], orPt[1]+self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, rg.Vector3d.ZAxis, orPt)
            brick.Transform(rot)
        return brick
    def drieklezoor (self, orPt, dir, header):
        basePlane = rg.Plane.WorldXY
        if dir>0:
            xSize = rg.Interval(orPt[0], orPt[0]+3*self.length/4)
        else:
            xSize = rg.Interval(orPt[0]-3*self.length/4, orPt[0])
        ySize = rg.Interval(orPt[1], orPt[1]+self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, rg.Vector3d.ZAxis, orPt)
            brick.Transform(rot)
        return brick
    def kop (self, orPt, dir, header):
        basePlane = rg.Plane.WorldXY
        if dir>0:
            xSize = rg.Interval(orPt[0], orPt[0]+self.length/2)
        else:
            xSize = rg.Interval(orPt[0]-self.length/2, orPt[0])
        ySize = rg.Interval(orPt[1], orPt[1]+self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, rg.Vector3d.ZAxis, orPt)
            brick.Transform(rot)
        return brick
    def klezoor (self, orPt, dir, header):
        basePlane = rg.Plane.WorldXY
        if dir>0:
            xSize = rg.Interval(orPt[0], orPt[0]+self.length/4)
        else:
            xSize = rg.Interval(orPt[0]-self.length/4, orPt[0])
        ySize = rg.Interval(orPt[1], orPt[1]+self.width)
        zSize = rg.Interval(orPt[2], orPt[2]+self.height)
        brick = rg.Box(basePlane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, rg.Vector3d.ZAxis, orPt)
            brick.Transform(rot)
        return brick

#Definitions
tolerance = 0.001
face = wall
bb = wall.GetBoundingBox(True)
bbMin = bb.Min
bbMax = rg.Point3d(bb.Min[0],bb.Min[1],bb.Max[2]-tolerance)
b = brick(brLength, brWidth, brHeight)
endP= []

#Wall creation
contours = rg.Brep.CreateContourCurves(wall, bbMin, bbMax, brHeight)
output = contours
bricks = []
counter = 0
halfC = []
points = []
for contour in contours:
    contour.Domain = rg.Interval(0,1)
    left = contour.Split(0.5)[0]
    right = contour.Split(0.5)[1]
    left.Reverse()
    halfC.append(left)
    halfC.append(right)
#------------------------------------------------------------------
#iteration through halves of curves: even numbers are left parts, odd numbers are right parts
for i in range(len(halfC)):
    current = halfC[i]
    curveLength1 = current.GetLength(tolerance)-(b.width)
    curveLength2 = current.GetLength(tolerance)
    t = current.DivideByLength(brLength/4, False)
    listL = len(t)
    if i%4==0 or i%4==1:
        even = True
    else:
        even = False
    if i%2==0:
        left = True
    else:
        left = False
    #--------------------------------------------------------------
    #iteration through parameters on halves of curves, j = 0 is one step after midpoint
    j = 0
    stop = False
    while j<listL and stop==False:
        #print "j:",j, "curveLength:", curveLength
        pt = current.PointAt(t[j])
        points.append(pt)
        #---------------------------------------------------------------------------------------------------
        #Even rows-stretcher pattern
        if even:
            if j%4==1:
                if curveLength1<b.length:
                    stop = True
            #-----------------------------------------------------------------------------
            #If stop is not true
            if stop == False:
                
                if j%4==1:
                    if left:
                        if j==1:
                            dir = 1
                            bricks.append(b.strek(pt,dir, False))
                            curveLength1 -= b.length/2
                            dir = -1
                    else:
                        if j==1:
                            curveLength1 -= b.length/2
                        dir = 1
                    bricks.append(b.strek(pt, dir, False))
                    curveLength1 -= b.length
                elif j%4==3:
                    if j>3:
                        bricks.append(last)
                    ptB = pt + rg.Vector3d(0, b.width, 0)
                    if left:
                        if j==3:
                            dir = 1
                            bricks.append(b.strek(ptB, dir, False))
                            dir = -1
                    else:
                        if j==3:
                            dir = -1
                            bricks.append(b.strek(ptB, dir, False))
                            dir = 1
                    last = b.strek(ptB, dir, False)
            #----------------------------------------------------------------------------
            #If stop is true
            else:
                if j%4==1:
                    if left:
                        dir = -1
                        bricks.append(b.custom(pt, dir, False, curveLength1, b.width, b.height))
                    else:
                        dir = 1
                        bricks.append(b.custom(pt, dir, False, curveLength1, b.width, b.height))
        #---------------------------------------------------------------------------------------
        #Odd rows - header pattern
        else:
            if j%2==0:
                if curveLength2<b.length:
                    stop = True
            if stop == False:
                if j%2==0:
                    if left:
                        if j==0:
                            dir = -1
                            bricks.append(b.strek(pt, dir, True))
                            curveLength2 -= b.length/4
                            dir = 1
                    else:
                        if j==0:
                            curveLength2 -= b.length/4
                        dir = -1
                    bricks.append(b.strek(pt, dir, True))
                    curveLength2 -= b.length/2
            #-------------------------------------------------------------------------------
            #If stop is True, end conditions
            else:
                if j%2==0:
                    if left:
                        dir = -1
                        bricks.append(b.custom(pt, dir, False, curveLength2, b.width, b.height))
        j +=1
    if left:
        dir = -1
        endPt = current.PointAt(0)
        if even:
            bricks.append(b.drieklezoor(endPt, dir, True))
            pt2 = endPt + rg.Vector3d(-dir*2*b.width, b.width, 0)
            bricks.append(b.klezoor(pt2, -dir, True))
        else:
            pt3 = endPt + rg.Vector3d(-dir*b.width, b.width, 0)
            bricks.append(b.custom(pt3, dir, True, b.width, curveLength2-b.width, b.height))

#Openings creation
newBricks = []
for brick in bricks:
    cnt = brick.Center
    stop = False
    for curve in curves:
        containment = curve.Contains(cnt, rg.Plane.WorldZX)
        if containment == rg.PointContainment.Inside:
            stop = True
    if stop==False:
        newBricks.append(brick)
bricks = newBricks

#Output
brickList = bricks