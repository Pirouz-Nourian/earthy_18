"""Creates brick walls for ward module.
    Inputs:
        module: The module as an open Brep (brep).
        brLength: The brick length (float).
        brWidth: The brick width (float).
        brHeight: The brick height (float).
        thick: A variable that indicates if the wall is thick (0.40 m) or not (0.20 m) (boolean).
    Output:
        brickWallFront: The front brick wall.
        brickWallBack: The back brick wall."""

__author__ = "nchristidi"
__version__ = "2018.11.05"

import Rhino.Geometry as rg
import math

class brick:
    def __init__ (self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
    def custom (self, plane, cLength, cWidth, cHeight):
        xSize = rg.Interval(0, cLength)
        ySize = rg.Interval(0, cWidth)
        zSize = rg.Interval(0, cHeight)
        brick = rg.Box(plane, xSize, ySize, zSize)
        return brick
    def strek (self, plane, header):
        orPt = plane.Origin
        xSize = rg.Interval(0, self.length)
        ySize = rg.Interval(0, self.width)
        zSize = rg.Interval(0, self.height)
        brick = rg.Box(plane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(math.pi/2, plane.ZAxis, orPt)
            brick.Transform(rot)
            vec = plane.XAxis
            dis = rg.Transform.Translation(vec*self.width)
            brick.Transform(dis)
        return brick
    def drieklezoor (self, plane, header):
        orPt = plane.Origin
        xSize = rg.Interval(0, 3*self.length/4)
        ySize = rg.Interval(0, self.width)
        zSize = rg.Interval(0, self.height)
        brick = rg.Box(plane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, plane.ZAxis, orPt)
            brick.Transform(rot)
            vec = plane.XAxis
            dis = rg.Transform.Translation(vec*self.width)
            brick.Transform(dis)
        return brick
    def kop (self, plane):
        orPt = plane.Origin
        xSize = rg.Interval(0, self.length/2)
        ySize = rg.Interval(0, self.width)
        zSize = rg.Interval(0, self.height)
        brick = rg.Box(plane, xSize, ySize, zSize)
        return brick
    def klezoor (self, plane, header):
        orPt = plane.Origin
        xSize = rg.Interval(0, self.length/4)
        ySize = rg.Interval(0, self.width)
        zSize = rg.Interval(0, self.height)
        brick = rg.Box(plane, xSize, ySize, zSize)
        if header:
            rot = rg.Transform.Rotation(dir*math.pi/2, plane.ZAxis, orPt)
            brick.Transform(rot)
            vec = plane.XAxis
            dis = rg.Transform.Translation(vec*self.length/4)
            brick.Transform(dis)
        return brick

def mainPattern (plane, bNum, streks):
    #brick class
    b = brick(brLength, brWidth, brHeight)
    
    #definitions
    orPt = plane.Origin
    bricksMain = []
    
    if streks:
        for i in range(bNum):
            basePlane = rg.Plane(orPt, plane.XAxis, plane.YAxis)
            bricksMain.append(b.strek(basePlane, False))
            orPt = orPt + plane.XAxis*b.length
    else:
        for i in range(bNum):
            basePlane = rg.Plane(orPt, plane.XAxis, plane.YAxis)
            if i%2==0:
                bricksMain.append(b.kop(basePlane))
                ptB = orPt + basePlane.YAxis*b.width
                basePlaneB = rg.Plane(ptB, basePlane.XAxis, basePlane.YAxis)
                bricksMain.append(b.strek(basePlaneB, True))
                ptC = orPt + basePlane.YAxis*(b.width+b.length)
                basePlaneC = rg.Plane(ptC, basePlane.XAxis, basePlane.YAxis)
                bricksMain.append(b.kop(basePlaneC))
            else:
                bricksMain.append(b.strek(basePlane, True))
                ptB = orPt + basePlane.YAxis*b.length
                basePlaneB = rg.Plane(ptB, basePlane.XAxis, basePlane.YAxis)
                bricksMain.append(b.strek(basePlaneB, True))
            orPt = orPt + plane.XAxis*b.width
    return bricksMain

def shortWall (wall, thick, tol):
    #brick class
    b = brick(brLength, brWidth, brHeight)
    #create contours
    wallBrep = wall.ToBrep()
    bb = wallBrep.GetBoundingBox(True)
    bbMin = bb.Min
    bbMax = rg.Point3d(bb.Min[0],bb.Min[1],bb.Max[2]-tol)
    contours = rg.Brep.CreateContourCurves(wallBrep, bbMin, bbMax, b.height)
    #definitions
    counter = 0
    bricks = []
    planes = []
    points = []
    normals = []
    tangents = []
    
    #loop
    #for i in range(0,2): #For checks
    for contour in contours:
        #reparametrize curve
        #contour = contours[i] #For checks when given an i within a range
        contour.Domain = rg.Interval(0,1)
        #define curve length
        crvLng = contour.GetLength(tol)
        #define starting point
        pt = contour.PointAt(1)
        points.append(pt) #For checks
        #define tangents
        tangvec = contour.TangentAt(0)
        tangvec.Reverse()
        tangents.append(tangvec) #For checks
        #define normals
        dest_pt= wall.ClosestPoint(pt)
        norm = wall.NormalAt(dest_pt[1], dest_pt[2])
        norm.Unitize()
        normals.append(norm) #For checks
        #define base plane
        basePlane = rg.Plane(pt, tangvec, norm)
        planes.append(basePlane)
        #define base planes of interior layers
        pt2 = pt + basePlane.YAxis*b.width + basePlane.XAxis*b.width
        basePlane2 = rg.Plane(pt2, tangvec, norm)
        pt3 = pt + basePlane.YAxis*2*b.width
        if counter%2==1:
            pt3 += basePlane.XAxis*2*b.length
        basePlane3 = rg.Plane(pt3, tangvec, norm)
        pt4 = pt + basePlane.YAxis*3*b.width + basePlane.XAxis*b.width
        basePlane4 = rg.Plane(pt4, tangvec, norm)
        
        #check if row is even or odd
        #------------------Even row
        if counter%2==0:
            bNum = int((crvLng/2-b.width)/b.length)*2
            customLng = (crvLng-2*b.width-bNum*b.length)/2
            #check if corner bricks need to be custom
            if abs(customLng-0.2)<tol:
                custom = False
                bNum += 2
            else:
                custom = True
            
            #Main fill
            #----Corner piece
            bricks.append(b.strek(basePlane,True))
            pt += basePlane.XAxis*b.width
            basePlane = rg.Plane(pt, tangvec, norm)
            #----Custom brick start
            if custom:
                bricks.append(b.custom(basePlane, customLng, b.width, b.height))
                pt += basePlane.XAxis*customLng
                basePlane = rg.Plane(pt, tangvec, norm)
                if customLng<b.width:
                    customLng2 = customLng+b.width
                else:
                    customLng2 = customLng-b.width
                bricks.append(b.custom(basePlane2, customLng2, b.width, b.height))
                customLng3 = (b.width+customLng)/2
                if thick:
                    bricks.append(b.custom(basePlane3, customLng3, b.width, b.height))
                    pt3 += basePlane3.XAxis*customLng3
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.custom(basePlane3, customLng3, b.width, b.height))
                    pt3 += basePlane3.XAxis*customLng3
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.custom(basePlane4, customLng2, b.width, b.height))
                    pt4 += basePlane.XAxis*customLng2
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
                else:
                    bricks.append(b.drieklezoor(basePlane3, False))
                    pt3 += basePlane3.XAxis*(3*b.length/4)
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.drieklezoor(basePlane3, False))
                    pt3 += basePlane3.XAxis*(3*b.length/4)
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.strek(basePlane3, True))
                    bricks.append(b.strek(basePlane4, False))
            #if customLng = 0.20m
            else:
                bricks.append(b.kop(basePlane2))
                bricks.append(b.drieklezoor(basePlane3, False))
                pt3 += basePlane3.XAxis*(3*b.length/4)
                basePlane3 = rg.Plane(pt3, tangvec, norm)
                bricks.append(b.drieklezoor(basePlane3, False))
                pt3 += basePlane3.XAxis*(3*b.length/4)
                basePlane3 = rg.Plane(pt3, tangvec, norm)
                if thick:
                    bricks.append(b.kop(basePlane4))
                    pt4 += basePlane4.XAxis*(b.length/2)
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
                else:
                    bricks.append(b.strek(basePlane3, True))
                    pt3 += basePlane3.XAxis*b.width
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.custom(basePlane4, customLng, b.width, b.height))
                    pt4 += basePlane4.XAxis*customLng
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
            
            #----Main pattern
            bricksMain = mainPattern(basePlane, bNum, (counter%2==0))
            pt += basePlane.XAxis*bNum*b.length
            basePlane = rg.Plane(pt, tangvec, norm)
            for current in bricksMain:
                bricks.append(current)
            #----Main pattern_Layer2
            if custom:
                pt2 += tangvec*customLng2
                if customLng<b.width:
                    bNum2 = bNum-1
                else:
                    bNum2 = bNum+1
            else:
                pt2 += tangvec*b.width
                bNum2 = bNum-1
            basePlane2 = rg.Plane(pt2, tangvec, norm)
            bricksMain = mainPattern(basePlane2, bNum2, (counter%2==0))
            pt2 += basePlane2.XAxis*(bNum2)*b.length
            basePlane2 = rg.Plane(pt2, tangvec, norm)
            for current in bricksMain:
                bricks.append(current)
            
            #----Main pattern_Layer3
            if custom:
                if thick:
                    bNum3 = bNum
            else:
                if thick:
                    bNum3 = bNum-2
                else:
                    bNum3 = bNum-3
            
            if thick:
                bricksMain = mainPattern(basePlane3, bNum3, (counter%2==0))
                pt3 += basePlane3.XAxis*bNum3*b.length
            else:
                if custom:
                    pt3 += basePlane3.XAxis*(crvLng-3*b.length-b.width)
                else:
                    pt3 += basePlane3.XAxis*bNum3*b.length
            basePlane3 = rg.Plane(pt3, tangvec, norm)
            
            for current in bricksMain:
                bricks.append(current)
            
            #----Main pattern_Layer4
            if custom:
                if thick:
                    if customLng>b.width:
                        bNum4 = bNum+1
                    else:
                        bNum4 = bNum-1
            else:
                if thick:
                    bNum4 = bNum-1
                else:
                    bNum4 = bNum-2
            if thick:
                bricksMain = mainPattern(basePlane4, bNum4, (counter%2==0))
                for current in bricksMain:
                    bricks.append(current)
                pt4 += basePlane4.XAxis*(bNum4*b.length)
                basePlane4 = rg.Plane(pt4, tangvec, norm)
            else:
                if custom:
                    pt4 += basePlane4.XAxis*(crvLng-2*b.length)
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
                else:
                    pt4 += basePlane4.XAxis*(bNum4*b.length)
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
            
            #----Custom brick end
            if custom:
                bricks.append(b.custom(basePlane, customLng, b.width, b.height))
                pt += basePlane.XAxis*customLng
                basePlane = rg.Plane(pt, tangvec, norm)
                bricks.append(b.custom(basePlane2, customLng2, b.width, b.height))
                if thick:
                    bricks.append(b.custom(basePlane3, customLng3, b.width, b.height))
                    pt3 += basePlane3.XAxis*customLng3
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.custom(basePlane3, customLng3, b.width, b.height))
                    bricks.append(b.custom(basePlane4, customLng2, b.width, b.height))
                    pt4 += basePlane4.XAxis*(customLng2)
                    basePlane4 = rg.Plane(pt4, tangvec, norm)
                else:
                    bricks.append(b.strek(basePlane3, True))
                    pt3 += basePlane3.XAxis*b.width
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.drieklezoor(basePlane3, False))
                    pt3 += basePlane3.XAxis*3*b.length/4
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.drieklezoor(basePlane3, False))
                    bricks.append(b.strek(basePlane4, False))
            else:
                bricks.append(b.kop(basePlane2))
                if thick:
                    bricks.append(b.kop(basePlane4))
                    
                else:
                    bricks.append(b.strek(basePlane3, True))
                    pt3 += basePlane3.XAxis*b.width
                    basePlane3 = rg.Plane(pt3,tangvec, norm)
                    bricks.append(b.strek(basePlane4, False))
                bricks.append(b.drieklezoor(basePlane3, False))
                pt3 += basePlane3.XAxis*(3*b.length/4)
                basePlane3 = rg.Plane(pt3, tangvec, norm)
                bricks.append(b.drieklezoor(basePlane3, False))
            #----Corner piece
            bricks.append(b.strek(basePlane,True))
            
        
        #------------------Odd row
        else:
            bNum = int((crvLng/2-2*b.width)/b.width)*2+1
            customLng = (crvLng-bNum*b.width)/2
            #check if corner bricks need to be custom
            if abs((customLng-b.width))<tol:
                custom = False
                bNum += 2
            else:
                custom = True
            
            #Main fill
            #----Starting conditions
            bricks.append(b.custom(basePlane, customLng, b.width, b.height))
            pt += basePlane.XAxis*customLng
            basePlane = rg.Plane(pt, tangvec, norm)
            bricks.append(b.custom(basePlane2, customLng-b.width, b.width, b.height))
            pt2 += basePlane2.XAxis*(customLng-b.width)
            basePlane2 = rg.Plane(pt2, tangvec, norm)
            if thick:
                if customLng<b.length:
                    bricks.append(b.custom(basePlane3, customLng-b.width, b.length, b.height))
                    pt3 += basePlane3.XAxis*(customLng-b.width)
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                else:
                    bricks.append(b.strek(basePlane3, True))
                    pt3 += basePlane3.XAxis*b.width
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
                    bricks.append(b.custom(basePlane3, customLng-b.width, b.length, b.height))
                    pt3 += basePlane3.XAxis*(customLng-b.width)
                    basePlane3 = rg.Plane(pt3, tangvec, norm)
            
            #----Main pattern
            for i in range(3):
                bricks.append(b.strek(basePlane, True))
                pt += basePlane.XAxis*b.width
                basePlane = rg.Plane(pt, tangvec, norm)
            if thick:
                bricksMain = mainPattern(basePlane, (bNum-6), (counter%2==0))
                pt += basePlane.XAxis*(bNum-6)*b.width
                basePlane = rg.Plane(pt, tangvec, norm)
                for current in bricksMain:
                    bricks.append(current)
            else:
                for i in range(bNum-6):
                    bricks.append(b.strek(basePlane, True))
                    pt += basePlane.XAxis*b.width
                    basePlane = rg.Plane(pt, tangvec, norm)
            for i in range(3):
                bricks.append(b.strek(basePlane, True))
                pt += basePlane.XAxis*b.width
                basePlane = rg.Plane(pt, tangvec, norm)
            pt2 += basePlane2.XAxis*bNum*b.width
            basePlane2 = rg.Plane(pt2, tangvec, norm)
            pt3 += basePlane3.XAxis*(bNum-7)*b.width
            basePlane3 = rg.Plane(pt3, tangvec, norm)
            
            #----Ending conditions
            bricks.append(b.custom(basePlane, customLng, b.width, b.height))
            if abs(customLng-b.width)>tol:
                bricks.append(b.custom(basePlane2, customLng-b.width, b.width, b.height))
                if thick:
                    if customLng<b.length:
                        bricks.append(b.custom(basePlane3, customLng-b.width, b.length, b.height))
                    else:
                        bricks.append(b.custom(basePlane3, customLng-b.length, b.length, b.height))
                        pt3 += basePlane3.XAxis*(customLng-b.length)
                        basePlane3 = rg.Plane(pt3, tangvec, norm)
                        bricks.append(b.strek(basePlane3, True))
        counter +=1
    return bricks, planes, contours, points, tangents


#definitions
tolerance = 0.001

#call function
walls = module.Faces
for i in range (walls.Count):
    wall = walls[i]
    if i==1:
        fw = shortWall(wall, thick, tolerance)
    if i==3:
        bw = shortWall(wall, thick, tolerance)

brickWallFront = fw[0]
brickWallBack = bw[0]
