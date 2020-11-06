import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
import Rhino

#lists
a=[]
ceilingList=[]
floorList=[]
xVectorScale=[]
yVectorScale=[]
roomXVector=[]
roomYVector=[]
xVS=[]
yVS=[]
basePlane=[]
bedroom=[]
couplesRoomsDimX=[]
couplesRoomsDimY=[]
floorCouplesRooms=[]
ceilingCouplesRooms=[]
originPointOffsets=[]
courtyardEdges=[]
divisionPoints=[]
countRoom=[]


#Singles Rooms

def createSingleRooms(z):
    a=math.sqrt(z*3.5)
    ceiling=math.ceil(a)
    floor=math.floor(a)
    ceilingList.append(ceiling)
    floorList.append(floor)

i=0

for i in singlesRooms:
    if i>4:
        x=i/2
        room1=math.ceil(x)
        room2=math.floor(x)
        countRoom.append(math.ceil(x/2))
        createSingleRooms(room1)
        createSingleRooms(room2)
    elif i==0:
        countRoom.append(0)
    else:
        x=i
        countRoom.append(1)
        createSingleRooms(x)

totalNumSinglesRoom=sum(countRoom)

#define rounding to even
def roundToEven(y):
    if y%2==0:
        return int(y)
    else:
        return int(y+1)

#X Vector Scale
for j in ceilingList:
    xVS=roundToEven(j)
    xVectorScale.append(xVS)
    j+=1

#Y Vector Scale
for k in floorList:
    yVS=roundToEven(k)
    yVectorScale.append(yVS)
    k+=1

#singles room dimensions/delete non rooms
for e in xVectorScale:
    if e>0:
        roomXVector.append(e)

for f in yVectorScale:
    if f>0.0:
        roomYVector.append(f)

#Couples Rooms
a=math.sqrt(7)
ceilingCouples=math.ceil(a)
floorCouples=math.floor(a)
ceilingCouplesRooms=roundToEven(ceilingCouples)
floorCouplesRooms=roundToEven(floorCouples)

if sum(couplesRooms)>0:
    for i in range((sum(couplesRooms))):
        roomXVector.append(ceilingCouplesRooms)
        roomYVector.append(floorCouplesRooms)
totalNumCouplesRoom=sum(couplesRooms)

#establish no of rooms
NumOfBedrooms=totalNumSinglesRoom+totalNumCouplesRoom

#basePlaneIndexes math
originPointOffset=[]
x=0
for i in roomYVector:
    x=x+i
    originPointOffset.append(x)

sumOffset=sum(roomYVector)

#Courtyard creation
xCourtyard=rg.Vector3d.XAxis
yCourtyard=rg.Vector3d.YAxis
courtyardOrigin=rg.Point3d.Origin
courtyardPlane=rg.Plane(courtyardOrigin,xCourtyard,yCourtyard)
if sumOffset<=28:
    courtyardGeo=rg.Rectangle3d(courtyardPlane,sumOffset-16,8)
else:
    courtyardGeo=rg.Rectangle3d(courtyardPlane,sumOffset-20,10)

courtyardCorners=[]
for i in range(1,4,1):
    if i<5:
        courtyardCorners.append(courtyardGeo.Corner(i))
        i+=1
    if i==4:
        courtyardCorners.append(courtyardGeo.Corner(0))

#divide courtyard circumference
courtyardCrv=rg.PolylineCurve(courtyardCorners)
divisionPoints=rg.Curve.DivideEquidistant(courtyardCrv,2.0)
divisionPointPlanes=[]

#creating planes
if len(divisionPoints)%2==0:
    lenDivisionPoints=len(divisionPoints)
else:
    lenDivisionPoints=len(divisionPoints)-1

if sumOffset<=28:
    for i in (0,5,1):
        planesA=rg.Plane(divisionPoints[i],rg.Vector3d.XAxis,rg.Vector3d.YAxis)
        divisionPointPlanes.append(planesA)
    for j in range (5,lenDivisionPoints-5,1):
        planesB=rg.Plane(divisionPoints[j],rg.Vector3d.YAxis,-rg.Vector3d.XAxis)
        divisionPointPlanes.append(planesB)
    for k in range (lenDivisionPoints-5,lenDivisionPoints+1,1):
        planesC=rg.Plane(divisionPoints[k],-rg.Vector3d.XAxis,-rg.Vector3d.YAxis)
        divisionPointPlanes.append(planesC)
    k+=1
else:
    for i in range(0,5,1):
        planesA=rg.Plane(divisionPoints[i],rg.Vector3d.XAxis,rg.Vector3d.YAxis)
        divisionPointPlanes.append(planesA)
    for j in range (6,int(lenDivisionPoints-4),1):
        planesB=rg.Plane(divisionPoints[j],rg.Vector3d.YAxis,-rg.Vector3d.XAxis)
        divisionPointPlanes.append(planesB)
    for k in range (lenDivisionPoints-4,lenDivisionPoints,1):
        planesC=rg.Plane(divisionPoints[k],-rg.Vector3d.XAxis,rg.Vector3d.YAxis)
        divisionPointPlanes.append(planesC)
planes=divisionPointPlanes

#forming rooms
bedrooms=[]
iter=int(NumOfBedrooms)

for x in range(0,iter,1):
    a=rg.Rectangle3d(divisionPointPlanes[int(originPointOffset[x]/2-1-originPointOffset[0])],roomXVector[x],roomYVector[x])
    bedrooms.append(a)

br=bedrooms
