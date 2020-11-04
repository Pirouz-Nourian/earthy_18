"""Creates REL chart from excel sheet.
        Inputs:
            displacement: REL chart distance from x-x' axis (float)
            tag_width: Space name tag width (float)
            tag_height: Space name tag height (float)
            tags: List of space names (str)
            matrix: Space connection values (ghdoc Object)
        Output:
            tag_plines: Tags curve outlines (Curve)
            or_pts: Space names origin points (Point3d)
            cells: REL chart diamond cell outlines (Curve)
            rel_symbols: REL chart space connection symbols (Curve)"""

__author__ = "nchristidi"
__version__ = "2018.09.20"

import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import Rhino as r
from copy import copy
import math

#create original text tag boundary
pts = (0,displacement,0),(tag_width,displacement,0),(tag_width+tag_height,displacement+tag_height,0),(tag_width,displacement+2*tag_height,0),(0,displacement+2*tag_height,0),(0,displacement,0)
pline = rs.AddPolyline(pts)


plines = [] #tags
locs = [] #text origin points

#iteration for array of text tags and text origin points
for i in range (len(tags)):
    trans_value = i*(-2*tag_height)
    vec = rg.Vector3d(0,trans_value,0)
    new_pl = rs.coercecurve(pline)
    new_pl.Translate(vec)
    plines.append(new_pl)
    
    pr = rg.AreaMassProperties.Compute(new_pl)
    cen = pr.Centroid
    vec = rg.Vector3d(1-tag_width/2,0,0)
    loc = cen+vec
    locs.append(loc)

#starting point for diamond cells
pt0 = rs.AddPoint(tag_width+tag_height,displacement+tag_height,0)

#functions for symbols
def DrawDiamond (orPt, edgeSize):
    orPt = rs.coerce3dpoint(orPt)
    pt1 = orPt + rg.Vector3d(edgeSize,-edgeSize,0)
    pt2 = orPt + rg.Vector3d(0, -2*edgeSize,0)
    pt3 = orPt + rg.Vector3d(-edgeSize, -edgeSize,0)
    pts = (orPt, pt1, pt2, pt3, orPt)
    diamond = rs.AddPolyline(pts)
    return diamond

def DrawTriangle(orPt, edgeSize):
    orPt = rs.coerce3dpoint(orPt)
    edgeSize = 1.5*edgeSize
    radius = (edgeSize*math.sqrt(3))/6
    vec = rg.Vector3d(0,radius,0)
    pt1 = orPt + vec
    vec = rg.Vector3d(radius, -2*radius,0)
    pt2 = pt1 + vec
    vec = rg.Vector3d(-2*radius, 0,0)
    pt3 = pt2 + vec
    pts = (pt1,pt2, pt3, pt1)
    triangle = rs.AddPolyline(pts)
    return triangle
    
def DrawSquare(orPt, edgeSize):
    orPt = rs.coerce3dpoint(orPt)
    edgeSize = 0.8 *edgeSize
    pts = []
    vec = rg.Vector3d(-edgeSize/2,edgeSize/2,0)
    pt1 = orPt+vec
    vec = rg.Vector3d(edgeSize, 0, 0)
    pt2 = pt1+vec
    vec = rg.Vector3d(0,-edgeSize,0)
    pt3 = pt2+vec
    vec = rg.Vector3d(-edgeSize,0,0)
    pt4 = pt3 + vec
    pts = (pt1,pt2,pt3,pt4,pt1)
    square = rs.AddPolyline(pts)
    return square

def DrawStar(orPt, edgeSize):
    orPt = rs.coerce3dpoint(orPt)
    edgeSize = 0.8*edgeSize
    inner = edgeSize/3
    
    pts = []
    
    vec = rg.Vector3d(-inner/2,inner/2,0)
    pt1 = orPt + vec
    vec = rg.Vector3d(inner/2,inner/2,0)
    pt3 = orPt + vec
    vec = rg.Vector3d(0,edgeSize,0)
    pt2 = orPt + vec
    
    vec = rg.Vector3d(inner/2,inner/2,0)
    pt4 = orPt + vec
    vec = rg.Vector3d(inner/2,-inner/2,0)
    pt6 = orPt + vec
    vec = rg.Vector3d(edgeSize,0,0)
    pt5 = orPt + vec
    
    vec = rg.Vector3d(inner/2,-inner/2,0)
    pt7 = orPt + vec
    vec = rg.Vector3d(-inner/2,-inner/2,0)
    pt9 = orPt + vec
    vec = rg.Vector3d(0,-edgeSize,0)
    pt8 = orPt + vec
    
    vec = rg.Vector3d(-inner/2,-inner/2,0)
    pt10 = orPt + vec
    vec = rg.Vector3d(-inner/2,inner/2,0)
    pt12 = orPt + vec
    vec = rg.Vector3d(-edgeSize,0,0)
    pt11 = orPt + vec
    
    pts = (pt1,pt2,pt3,pt4,pt5,pt6,pt7,pt8,pt9,pt10,pt11,pt12)
    star = rs.AddPolyline(pts)
    return star


diamonds = [] #list of diamonds
diaCnt = [] #list of center points of diamonds
lng = 2*(len(tags)-1) #two times the number of cells in first column, because diamonds are arranged also in half-rows

#iteration
for i in range (len(tags)-1): #zero to columns number minus one (number of columns)
    #print "i:",i
    j = i
    while j<lng:
        #print "j:", j
        orPt = rs.coerce3dpoint(pt0)
        orPt = orPt + rg.Vector3d(tag_height*i, -tag_height*j, 0)
        pline1 = DrawDiamond (orPt, tag_height)
        pline1 = rs.coercecurve(pline1)
        diamonds.append(pline1) #adds to list of diamonds
        
        prp = rg.AreaMassProperties.Compute(pline1)
        cnt = prp.Centroid
        diaCnt.append(cnt) #adds to list of diamond center points
        j += 2 #skips a half-row
    lng = lng-1 #in every iteration the number of rows decreases by one to create triangle


k = matrix.BranchCount
diaNumber = int((pow(k,2)-k)/2) #number of diamonds based on number of text tags (triangular stacking)

#function that finds index based on the particular arrangement, using as given the indexes of the two spaces and the number of spaces
def IndexFind(a,b,k):
    end = b-a
    l = 0
    for i in range(end):
        l += k-(i+1)
    result = l-(k-b)
    return result

#iteration for drawing symbols
indexes = []
symbols = []
for i in range (k):
    column = matrix.Branch(i)
    for j in range (k):
        if i>j:
            rel = column[j]
            #print rel
            index = IndexFind(j,i,k)
            #print "i:",i,"j:",j,"index:",index
            indexes.append(index)
            if (rel=="1"):
                cir = rs.AddCircle(rg.Plane(diaCnt[index],rg.Vector3d.ZAxis),tag_height/2)
                symbols.append(cir)
            elif (rel == "0.75"):
                diamond = DrawTriangle(diaCnt[index],tag_height)
                symbols.append(diamond)
            elif (rel == "0.5"):
                square = DrawSquare(diaCnt[index],tag_height)
                symbols.append(square)
            elif (rel == "0.25"):
                star = DrawStar(diaCnt[index],tag_height)
                symbols.append(star)
            else:
                continue

#output
tag_plines = plines
or_pts = locs
cells = diamonds
rel_symbols = symbols