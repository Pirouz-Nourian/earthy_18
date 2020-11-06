import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

#construct shape of pavillion
point1 = rs.AddPoint(0,0,0)
point2 = rs.AddPoint(0,0,3)
pavillionHeight = 4
spiralBottom = rs.AddSpiral(point1,point2,0,1.25,2,3)
spiralTop = rs.OffsetCurve(spiralBottom, [1,0,0],1.5)
rs.MoveObject(spiralTop,[0.5,0,pavillionHeight])
pavillionShape = rs.AddLoftSrf([spiralBottom,spiralTop])

# construct brick
brickHeight = 0.057
brickLength = 0.203
brickWidth = 0.092
pointA = rs.AddPoint(0,0,0)
pointB = rs.AddPoint(brickLength,0,0)
pointC = rs.AddPoint(brickLength,brickWidth,0)
pointD = rs.AddPoint(0,brickWidth,0)
pointE = rs.AddPoint(0,0,brickHeight)
pointF = rs.AddPoint(brickLength,0,brickHeight)
pointG = rs.AddPoint(brickLength,brickWidth,brickHeight)
pointH = rs.AddPoint(0,brickWidth,brickHeight)
brickVertexes = [pointA, pointB, pointC, pointD, pointE, pointF, pointG, pointH]

#construct slices and define coordinates to insert bricks
xyPlane = rs.WorldXYPlane()
sectionPlane = rs.AddPlaneSurface(xyPlane,20,20)
rs.MoveObject(sectionPlane, [-10,-10,0])
brickInsertionPointsA = []
h=0
i=0
while h<pavillionHeight:
    sectionPlaneMoved = rs.CopyObject(sectionPlane,[0,0,h])
    sectionCurve = rs.IntersectBreps(pavillionShape, sectionPlaneMoved)
    if i%2 ==0:
        rs.ExtendCurveLength(sectionCurve,2,2,(0.5*brickLength)) #extend every second sectioncurve in order to create a proper brick overlap of half a bricklength
    sectionCurve2 = rs.DivideCurveEquidistant(sectionCurve,brickLength,True,True)
    brickInsertionPoint = rs.DivideCurve(sectionCurve, (len(sectionCurve2)),True,True)
    brickInsertionPointsA.extend(brickInsertionPoint)
    h += brickHeight
    i += 1

#inserting bricks
brickInsertionPointsB = brickInsertionPointsA[1:]
numberOfBricks = len(brickInsertionPointsB)
bricks = []
n=0
while n<numberOfBricks:
    A = brickInsertionPointsA [n]
    B = brickInsertionPointsB [n]
    Distance = rs.Distance(A,B)
    if Distance < (brickLength+0.1):
        translationVector = rs.VectorCreate(A,pointA)
        rs.MoveObjects(brickVertexes,translationVector)
        brick = rs.AddBox(brickVertexes)
        rAngle = rs.Angle(A,B)
        rs.RotateObject(brick, A, (rAngle[0]))
        bricks.append(brick)
    n +=1
