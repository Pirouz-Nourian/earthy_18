"""
Create and place the ward module, for the semi - private rooms (2 rooms). That typology consists
of two rooms(left and right room), 3x6m each. 
    Inputs:
        opening_01: The curve for the opening for the right and left wall (curve).
        opening_02: The curve for the opening for the front and interior wall (curve).
        opening_03: The curve for the opening (window) for the interior wall (curve).
        wards_crvs: The curves (plan view) for the semi - private rooms (list of curves).
        courtyards_crvs: The curves (plan view) for the courtyards (list of curves).
        labs_crv: The curves (plan view) of the laboratory department (curve). 
        nursery_crv: The curves (plan view) of the nursery department (curve).
        boundary_crv: The outline of the floor plan (curve).
        backOpeningsNumber: The number of the openings on the back wall (int).
        backOpeningsSize: The size of the openings on the back wall (float).
    Output:
        modularConfig: The modules (Brep).
"""
__author__ = "Despoina Pouniou, Nikoletta Christidi"
__version__ = "2018.10.28"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Collections as rc
from copy import copy
import math

#Create the openings for the back wall
def createSquare(point, size):
    pt1 = point + rg.Vector3d(size/2, size/2, 0)
    pt2 = point + rg.Vector3d(-size/2, size/2, 0)
    pt3 = point + rg.Vector3d(-size/2, -size/2, 0)
    pt4 = point + rg.Vector3d(size/2, -size/2,0)
    sqrPts = [pt1,pt2,pt3,pt4,pt1]
    square = rs.AddPolyline(sqrPts)
    square = rs.coercecurve(square)
    square.Rotate(math.pi/2, rg.Vector3d.XAxis, point)
    return square

"""
Define the class Module, to create the semi - private rooms. That class contains the functions to create the 
5 walls and the floor of each room. It also contains a function to make BooleanUnion of these geometries, and place them in the floor plan. 
"""
class Module:
    def __init__ (self, orPt, outside):
        self.length = 6.00
        self.width = 3.00
        self.thickness = 0.20
        self.height = 3.00
        vecOrPt = rg.Vector3d(-self.width/2,-self.length/2,0)
        self.orPt = orPt + vecOrPt
        if outside:
            self.thicknessBW = self.thickness*2
        else:
            self.thicknessBW = self.thickness
            
    #Define the floor for each room.
    def floor(self):
        vecFL = rg.Vector3d(0,0,-self.thickness)
        orPtFL = self.orPt + vecFL
        xSize = rg.Interval(0, self.width)
        ySize = rg.Interval(0, self.length)
        zSize = rg.Interval(0, self.thickness)
        plane = rg.Plane(orPtFL, rg.Vector3d.ZAxis)
        fl = rg.Box(plane, xSize, ySize, zSize)
        floorBrep = fl.ToBrep()
        return floorBrep
    """"
    Define a function for the back wall for each room.The arguments of the function are 1.the existence of openings(openings), 
    2.the number of openings(backOpNum) and 3.the openings'size(backOpSize).
    """
    def backWall(self, openings, backOpNum, backOpSize):
        if left:
            vecBW = rg.Vector3d(self.thickness, 0,0)
            xSize = rg.Interval(0, self.width-2*self.thickness)
        elif left == False:
            vecBW = rg.Vector3d(0, 0,0)
            xSize = rg.Interval(0, self.width)
        orPtBW = self.orPt + vecBW
        ySize = rg.Interval(0, self.thicknessBW)
        zSize = rg.Interval(0, self.height)
        plane = rg.Plane(orPtBW, rg.Vector3d.ZAxis)
        bw = rg.Box(plane, xSize, ySize, zSize)
        bwBrep = bw.ToBrep()
        if openings:
            self.backOpNum = backOpNum
            self.backOpSize = backOpSize
            divLength = self.width/(self.backOpNum+1)
            squares = rc.CurveList()
            extrusions = []
            for i in range(self.backOpNum):
                 pt = self.orPt + rg.Vector3d((i+1)*divLength,0,2)
                 sq = createSquare(pt, self.backOpSize)
                 sq1 = copy(sq)
                 sq1.Translate(0,self.thicknessBW,0)
                 squares.Add(sq)
                 squares.Add(sq1)
                 extr = rg.Brep.CreateFromLoft(squares, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False)
                 squares.Clear()
                 extrusions.append(extr)
            for i in range(len(extrusions)):
                bw = rg.Brep.CreateBooleanDifference(bwBrep, extrusions[i][0], 0.001)
                backWall = rg.Brep.CreateBooleanDifference(bw[0], extrusions[i][0], 0.001)
                bwBrep = backWall[0]
        else:
            backWall = bwBrep
        if type(backWall) is not rg.Brep:
            backWall = backWall[0]
        return backWall

#Define a function for the front wall for each room.
    def frontWall(self):
        vecFW = rg.Vector3d(0, self.length-self.thickness, 0)
        orPtFW = self.orPt + vecFW
        xSize = rg.Interval(0, self.width)
        ySize = rg.Interval(0, self.thickness)
        zSize = rg.Interval(0, self.height)
        plane = rg.Plane(orPtFW, rg.Vector3d.ZAxis)
        frontwallPlain = rg.Box(plane, xSize, ySize, zSize)
        curves = rc.CurveList()
        orPtOpening_01 = orPtFW + rg.Vector3d(self.width/2,0,0) 
        curve1 = opening_02
        start = curve1.PointAtStart
        end = curve1.PointAtEnd
        plane0=rg.Plane(start, end, start + rg.Vector3d(0,1,0))
        plane1=rg.Plane(orPtFW + rg.Vector3d(self.width/2,0,0) - rg.Vector3d(1.5/2,0,0),orPtFW + rg.Vector3d(self.length-self.thickness, 0, 0), orPtFW + rg.Vector3d(0, self.thickness, 0))
        orient = rg.Transform.PlaneToPlane(plane0, plane1)
        curve1.Transform(orient)
        curve2 = copy(curve1)
        curve2.Translate(0, self.thickness,0)
        loftCrvs = rc.CurveList()
        loftCrvs.Add(curve1)
        loftCrvs.Add(curve2)
        extr = rg.Brep.CreateFromLoft(loftCrvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False)
        fwPlainBrep = frontwallPlain.ToBrep()
        extr = extr[0]
        frontWall = rg.Brep.CreateBooleanDifference(fwPlainBrep, extr, 0.001)
        frontWall = rg.Brep.CreateBooleanDifference(fwPlainBrep, frontWall[0], 0.001)
        frontWall = frontWall[0]        
        return frontWall

#Define a function for the left wall for each room.
    def leftWall(self, leftNeighbour):
        orPtLW = self.orPt 
        xSize = rg.Interval(0, 2*self.thickness)
        ySize = rg.Interval(0, self.length-self.thickness)
        zSize = rg.Interval(0, self.height)
        plane = rg.Plane(orPtLW, rg.Vector3d.ZAxis)
        leftWallPlain = rg.Box(plane, xSize, ySize, zSize)
        corWidth = (self.length-self.thickness)-((2*self.length/3)+self.thickness/2)
        orPtOpening1 = orPtLW + rg.Vector3d(0, (2*self.length/3)+(self.thickness/2+corWidth/2)- 1.5/2,0)
        curve1 = opening_01
        start = curve1.PointAtStart
        end = curve1.PointAtEnd
        plane0=rg.Plane(start, end, start + rg.Vector3d(1,0,0))
        plane1=rg.Plane(orPtOpening1, orPtOpening1 + rg.Vector3d(0,self.thickness,0),orPtOpening1 + rg.Vector3d(self.thickness,0,0))
        lwPlainBrep = leftWallPlain.ToBrep()
        orient = rg.Transform.PlaneToPlane(plane0, plane1)
        curve1.Transform(orient)
        curve2 = copy(curve1)
        curve2.Translate(2*self.thickness,0,0)
        loftCrvs = rc.CurveList()
        loftCrvs.Add(curve1)
        loftCrvs.Add(curve2)
        extr = rg.Brep.CreateFromLoft(loftCrvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False)
        extr = extr[0]
        leftW = rg.Brep.CreateBooleanDifference(lwPlainBrep, extr, 0.001)
        #If leftNeighbour is True, then create a second opening, for access to the adjacent room.
        if leftNeighbour:
            extr01 = extr
            extr01.Translate(rg.Vector3d(0,-2.1,0))
            leftWall = rg.Brep.CreateBooleanDifference(leftW[0], extr01, 0.001)
            leftWall=leftWall[0]
        else:
            leftWall = leftW[0]
        return leftWall

    #Define a function for the right wall for each room.
    def rightWall(self, rightNeighbour):
        vecRW = rg.Vector3d(self.width-2*self.thickness, 0, 0)
        orPtRW = self.orPt + vecRW
        xSize = rg.Interval(0, 2*self.thickness)
        ySize = rg.Interval(0, self.length-self.thickness)
        zSize = rg.Interval(0, self.height)
        plane = rg.Plane(orPtRW, rg.Vector3d.ZAxis)
        rightWallPlain = rg.Box(plane, xSize, ySize, zSize)
        corWidth = (self.length-self.thickness)-((2*self.length/3)+self.thickness/2)
        orPtOpening1 = orPtRW + rg.Vector3d(0, (2*self.length/3)+(self.thickness/2+corWidth/2)-1.5/2,0)
        curves = rc.CurveList()
        curve1 = opening_01
        start = curve1.PointAtStart
        end = curve1.PointAtEnd
        plane0=rg.Plane(start, end, start + rg.Vector3d(1,0,0))
        plane1=rg.Plane(orPtOpening1, orPtOpening1 + rg.Vector3d(0,self.thickness,0),orPtOpening1 + rg.Vector3d(self.thickness,0,0))
        orient = rg.Transform.PlaneToPlane(plane0, plane1)
        curve1.Transform(orient)
        curve2 = copy(curve1)
        curve2.Translate(2*self.thickness,0,0)
        loftCrvs = rc.CurveList()
        loftCrvs.Add(curve1)
        loftCrvs.Add(curve2)
        extr = rg.Brep.CreateFromLoft(loftCrvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False)
        extr = extr[0]
        rwPlainBrep = rightWallPlain.ToBrep()
        rightW = rg.Brep.CreateBooleanDifference(rwPlainBrep, extr, 0.001)
        rightW = rightW[0]
        #If rightNeighbour is True, then create a second opening, for access to the adjacent room.
        if rightNeighbour:
            extr01 = extr
            extr01.Translate(rg.Vector3d(0,-2.1,0))
            rightWall = rg.Brep.CreateBooleanDifference(rightW, extr01, 0.001)
            rightWall = rightWall[0]
        else:
            rightWall = rightW
        return rightWall

    #Define a function for the interior wall for each room.
    def interWall(self, left):
        vecIW = rg.Vector3d(2*self.thickness, (self.length*2/3)-1.5*self.thickness,0)
        orPtIW = self.orPt + vecIW
        xSize = rg.Interval(0, self.width-4*self.thickness)
        ySize = rg.Interval(0, 2*self.thickness)
        zSize = rg.Interval(0, self.height)
        plane = rg.Plane(orPtIW, rg.Vector3d.ZAxis)
        interwallPlain = rg.Box(plane, xSize, ySize, zSize)
        iwPlainBrep = interwallPlain.ToBrep()
        curves = rc.CurveList()
        """
        Check if the room is a left or a right room. If it is a left one,
        place a window (opening_03), and if it is a right one place a door (opening_02).
        """
        if left:
            curve1 = opening_03
            curve1_5 = curve1.DuplicateSegments()[0]
            start = curve1_5.PointAtStart
            end = curve1_5.PointAtEnd
            plane0=rg.Plane(start, end, start + rg.Vector3d(0,1,0))
            plane1=rg.Plane(orPtIW + rg.Vector3d(self.width/2 - self.thickness ,0,0.9) - rg.Vector3d(1.5/2,0,0),orPtIW + rg.Vector3d(self.length-self.thickness, 0, 0.9), orPtIW + rg.Vector3d(0, self.thickness, 0.9))
            orient = rg.Transform.PlaneToPlane(plane0, plane1)
            curve1.Transform(orient)
            curve2 = copy(curve1)
            curve2.Translate(0, 2*self.thickness,0)
            loftCrvs = rc.CurveList()
            loftCrvs.Add(curve1)
            loftCrvs.Add(curve2)
        else:
            curve1 = opening_02
            start = curve1.PointAtStart
            end = curve1.PointAtEnd
            plane0=rg.Plane(start, end, start + rg.Vector3d(0,1,0))
            plane1=rg.Plane(orPtIW + rg.Vector3d(self.width/2 - 2*self.thickness,0,0) - rg.Vector3d(1.5/2,0,0),orPtIW + rg.Vector3d(self.length-self.thickness, 0, 0), orPtIW + rg.Vector3d(0, self.thickness, 0))
            orient = rg.Transform.PlaneToPlane(plane0, plane1)
            curve1.Transform(orient)
            curve2 = copy(curve1)
            curve2.Translate(0, 2*self.thickness,0)
            loftCrvs = rc.CurveList()
            loftCrvs.Add(curve1)
            loftCrvs.Add(curve2)
        extr = rg.Brep.CreateFromLoft(loftCrvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False)
        extr = extr[0]
        interWall = rg.Brep.CreateBooleanDifference(iwPlainBrep, extr, 0.001)
        interWall = rg.Brep.CreateBooleanDifference(iwPlainBrep, interWall[0], 0.001)
        if type(interWall) is not rg.Brep:
            interWall = interWall[0]
        return interWall
        """
        The function makeModule makes a BooleanUnion of the 5 walls and the floor for each room. 
        Then, it orients the room according to the closest courtyard to it.  
        """
    def makeModule(self, walls, vecF):
        module = rg.Brep.CreateBooleanUnion(walls, 0.001)
        vecFrontMod = rg.Vector3d.YAxis
        angle = rg.Vector3d.VectorAngle(vecFrontMod, vecF, rg.Vector3d.ZAxis)
        module = module[0]
        module.Rotate(angle, rg.Vector3d.ZAxis, orPt)
        return module


centers = []
cps = []
vecs = []
modules = []
count = 0
left = True
#(In general) Iterate through the list of wards_crvs, and create and place an object of the class Module for each curve.
#For each curve in wards_crvs, find the center point.
for ward in wards_crvs:
    prp = rg.AreaMassProperties.Compute(ward)
    cnt = prp.Centroid
    centers.append(cnt)
""""
Create a counter inside the for loop of the wards_crvs, to seperate the left rooms
from the right rooms, and assign them different properties.
"""
for i in range(len(wards_crvs)):
    if count == 0:
        left = True
        count = 1
    elif count == 1:
        left = False
        count = 0
    #(In general) Iterate through the list of courtyards_crvs, and find the closest courtyard curve(j) to the ward curve(i).
    #For each curve in courtyards_crvs, find the closest point to the center point of each curve in wards_crvs.
    for j in range(len(courtyards_crvs)):
        param = courtyards_crvs[j].ClosestPoint(centers[i])[1]
        cp = courtyards_crvs[j].PointAt(param)
        cps.append(cp)
    #For each center point in centers, find the min distance to the closest point of the courtyards_crvs.
    for j in range (len(cps)):
        if j == 0:
            distance = centers[i].DistanceTo(cps[j])
            closest = cps[j]
        else:
            distCheck = centers[i].DistanceTo(cps[j])
            if distCheck<distance:
                distance = distCheck
                closest = cps[j]
    cps.Clear()
    #For each curve in wards_crvs, define a vector(vecToFront) in reference to the closest courtyard. 
    vecToFront = closest - centers[i]
    vecs.append(vecToFront)
    #For each curve in wards_crvs, define 2 other vectors(vecToLeft and vecToBack) to check for adjacencies. 
    rotAxis = rg.Point3d(centers[i][0], centers[i][1], centers[i][2]+1.0)-centers[i]
    vecToLeft = copy(vecToFront)
    vecToLeft.Rotate(math.pi/2, rotAxis)
    vecToLeft.Unitize()
    vecToBack = copy(vecToFront)
    vecToBack.Rotate(math.pi, rotAxis)
    vecToBack.Unitize()
    transCenterL = centers[i]+vecToLeft*3.00
    transCenterR = centers[i]-vecToLeft*3.00
    transCenterB = centers[i] + vecToBack*6.00
    leftN = False
    rightN = False
    backN = False 
    boundaryP = True 
    backOp = True
    #(In general)Check for adajcencies.
    #If another curve in wards_crvs contains the moved center to the left, then leftN = True.
    #If another curve in wards_crvs contains the moved center to the right, then rightN = True.
    #If the lab or nursery curve contains the moved center to the back, then backOp = True.
    #If the boundary curve contains the moved center to the back, then boundaryP = True.
    for j in range(len(wards_crvs)):
        if i!=j:
            if (abs(transCenterL[0]-centers[j][0])<0.001) and (abs(transCenterL[1]-centers[j][1])<0.001) and (abs(transCenterL[2]-centers[j][2])<0.001):
                leftN = True
            if (abs(transCenterR[0]-centers[j][0])<0.001) and (abs(transCenterR[1]-centers[j][1])<0.001) and (abs(transCenterR[2]-centers[j][2])<0.001):
                rightN = True
    containment = boundary_crv.Contains(transCenterB, rg.Plane.WorldXY, 0.001)
    if (containment==rg.PointContainment.Inside):
        boundaryP = False
    containment1 = labs_crv.Contains(transCenterB, rg.Plane.WorldXY, 0.001)
    containment2 = nursery_crv.Contains(transCenterB, rg.Plane.WorldXY, 0.001)
    if (containment1==rg.PointContainment.Inside) or (containment2==rg.PointContainment.Inside):
        backOp = False
        
#Create an object, m, of the class Module.
    orPt = centers[i]
    m = Module(orPt, boundaryP)
    walls = []
    bw = m.backWall(backOp, backOpeningsNumber, backOpeningsSize)
    walls.append(bw)
    walls.append(m.frontWall())    
    walls.append(m.leftWall(leftN))
    walls.append(m.rightWall(rightN))
    walls.append(m.interWall(left))
    walls.append(m.floor())
    mod = m.makeModule(walls, vecToFront)
    modules.append(mod)
    walls.Clear()


modularConfig = modules

