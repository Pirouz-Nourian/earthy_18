import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


#construct cone

pt1 = rs.AddPoint(0,0,0)
pt2 = rs.AddPoint(0,0,1)
height = 6000
radius = 1500
spiral1 = rs.AddSpiral(pt1,pt2,0,1,1000,3000)
spiral2 = rs.AddSpiral(pt1,pt2,0,1,30,90)
rs.MoveObject(spiral2,[0,0,height])

cone1 = rs.AddLoftSrf([spiral1,spiral2])

#brick vertices
brickHeight = 57
brickLength = 203
brickWidth = 92
pointA = rs.AddPoint(0,0,0)
pointB = rs.AddPoint(brickLength,0,0)
pointC = rs.AddPoint(brickLength,brickWidth,0)
pointD = rs.AddPoint(0,brickWidth,0)
pointE = rs.AddPoint(0,0,brickHeight)
pointF = rs.AddPoint(brickLength,0,brickHeight)
pointG = rs.AddPoint(brickLength,brickWidth,brickHeight)
pointH = rs.AddPoint(0,brickWidth,brickHeight)
brickVertexes = [pointA, pointB, pointC, pointD, pointE, pointF, pointG, pointH]


#getting points for brick placement
contours=[]
contours = rs.AddSrfContourCrvs(cone1,([0,0,0], [0,0,6000]), interval=57)
length = 203
mycurvesA=[]
framesA=[]
i=0
while i < len(contours) :
    if i%2 == 0:
        rs.ExtendCurveLength(contours[i],2,0,0.5*brickLength)
    mycurves= rs.DivideCurveEquidistant(contours[i],length*1.25-((i*9)%7),True,True)
    mycurvesA.extend(mycurves)
    i+=1

#place bricks

mycurvesB = mycurvesA[1:]
numberOfBricks = len(mycurvesB)
bricks = []
n=0
while n<numberOfBricks:
    A = mycurvesA [n]
    B = mycurvesB [n]
    Distance = rs.Distance(A,B)
    if Distance < (203+100):
        translationVector = rs.VectorCreate(A,pointA)
        rs.MoveObjects(brickVertexes,translationVector)
        myBrick = rs.AddBox(brickVertexes)
        rAngle = rs.Angle(A,B)
        rs.RotateObject(myBrick, A, (rAngle[0]))
        bricks.append(myBrick)
    n +=1