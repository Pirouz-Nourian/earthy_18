#author:Ammar_Taher
#Date:14/09/2018
#TU_Delft_BK_BT
#student_number:4745639

import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib
import math

#logic of algorithm
#contour curve create
#for curves list each item should be divided into points 
#evaluate each point to get the plane on it
#create the brick on the plane oriented with the tangent to this point parameter

#1_contour on the brep planes
height= (house.GetBoundingBox(house)).Max[2]
start= (house.GetBoundingBox(house)).Min[2]
b= rg.Point3d(0,0,start)                    #beginning of contour
e= rg.Point3d(0,0,height)                   # end of contour 
contours= house.CreateContourCurves(house,b,e,sH)

#2_divide the contours into points and create the brick at it
ptlist=[]
contourpts=[]
f=[]  
CPt=[]
bricks=[]

for i in contours:
    XC= math.ceil(i.GetLength()/((sW)**2+(sL)**2)**0.5)
    pt= i.DivideByCount(XC,True)
    ptlist.append(pt)
    for pts in pt:                          #this beacuse we want to access the points at the parameter of each point in the list
        point=i.PointAt(pts)
        CPt.append(point)
        (bool,frames)=i.FrameAt(pts)        # 3_add bool list to recieve the boolen values and frames recieve the frames
        f.append(frames)
        x=rg.Interval(0,sW)                 #creating the brick size
        y=rg.Interval(0,sL)
        z=rg.Interval(0,sH)
        brick=rg.Box(frames,x,y,z)          # 4_using frames makes it easier to align with the tangent to the curve
        bricks.append(brick)
        contourpts.append(pts)

brick= bricks
Cpt=CPt
Cpt_frame= f