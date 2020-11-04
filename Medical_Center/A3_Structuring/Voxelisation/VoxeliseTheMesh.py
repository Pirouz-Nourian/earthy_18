"""Provides a scripting component.
    Inputs:
        x: Voxel resolution in x
        y: Voxel resolution in y
        z: Voxel resolution in z
        tol: Tolerance distance to mesh
    Output:
        voxels: Voxel output"""

__author__ = "erron estrado"
__version__ = "2018.10.19"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Grasshopper as gh
import math
from copy import copy


def MakeBrick(orPt, xSize, ySize, zSize):
    plane = rg.Plane(orPt, rg.Vector3d.ZAxis)
    X = rg.Interval(0, xSize)
    Y = rg.Interval(0, ySize)
    Z = rg.Interval(0, zSize)
    brk = rg.Box(plane, X, Y, Z)
    return brk

def TestCloseness(testPt, testMesh, tolerance):
    meshPt = testMesh.ClosestPoint(testPt)
    dist = testPt.DistanceTo(meshPt)
    if dist <= tolerance:
        return True
    else:
        return False

def Voxelise(mesh, xRes, yRes, zRes, iTol):
    # Make bounding box to voxelise and get start position
    box = mesh.GetBoundingBox(False)
    startPt = box.Min
    
    # initialise lists and variables
    layer = 0
    bricks = []
    pt = copy(startPt)
    
    # initialise data tree
    brickTree = gh.DataTree[rg.Box]()
    
    # Z direction
    while box.Contains(pt) :
        
        # Y direction
        while box.Contains(pt): 
        
            # X direction
            while box.Contains(pt): 
                # if too far skip
                isClose = TestCloseness(pt, mesh, iTol)
                if isClose == False:
                    pt.X += xRes
                    continue
                #if even numbered layer make brick horizontal if odd vertical brick
                if layer%2 == 0:
                    b = MakeBrick(pt, 4*xRes, 2*yRes, zRes)
                    bricks.append(b)
                    pt.X += 4*xRes
                else:
                    b = MakeBrick(pt, 2*xRes, 4*yRes, zRes)
                    bricks.append(b)
                    pt.X += 2*xRes
            # reset x position and advance in y
            pt.X = startPt.X
            if layer%2 == 0:
                pt.Y += 2*yRes
                #pt.X += xRes
            else:
                pt.Y += 4*yRes
                #pt.X += xRes
        # add layer to new branch of data tree and clear list
        for v in bricks:
            brickTree.Add(v,gh.Kernel.Data.GH_Path(layer))
        bricks.Clear()
        
        # reset y position and advance in z
        if layer%2 == 0:
                pt.Y = startPt.Y + yRes
        else:
            pt.Y = startPt.Y
        #pt.Y = startPt.Y
        layer += 1
        pt.Z += zRes
    return brickTree


wrkingMesh = Mesh
brk = Voxelise(wrkingMesh, x, y, z, tol)

voxels = brk