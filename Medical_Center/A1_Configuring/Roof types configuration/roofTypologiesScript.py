"""Creates roof configuration based on lookup table.
    Inputs:
        roofMatrix: The 2D matrix (as a tree) containing the configuration (int).
        pts: The grid points (as a tree) where the roof units are placed (Point3d).
        roofTypes: The list of roof types.
    Output:
        roofs: The roof configuration."""

__author__ = "nchristidi"
__version__ = "2018.09.28"

#Libraries
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
from copy import copy

#Definitions
orPoint = rg.Point3d(0,0,0)
stPoints = []
roofs = []

#Create starting points list
for i in range(pts.BranchCount-1):
    branchList = pts.Branch(i)
    
    for j in range(branchList.Count-1):
        stPoints.append(branchList[j])

#Main loop
for i in range(len(roofTypes)):
    roofTypes[i] = rs.coercebrep(roofTypes[i])
for i in range(roofMatrix.BranchCount):
    branchList = roofMatrix.Branch(i)
    pointsColumn = pts.Branch(i)
    for j in range(branchList.Count):
        currentPt = pointsColumn[j]
        vector = currentPt - orPoint
        pointer = branchList[j]
        roofCopy = copy(roofTypes[pointer])
        roofCopy.Translate(vector)
        roofs.append(roofCopy)