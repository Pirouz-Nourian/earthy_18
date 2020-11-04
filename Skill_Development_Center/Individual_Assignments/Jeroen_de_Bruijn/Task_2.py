"""Explodes the piglet's house
    Inputs:
        house: the piglet's house brep
    Output:
        exploded: exploded faces
        not_exploded: not exploded faces"""

__author__ = "Mr. Wolf"
__version__ = "2018.09.04"

import rhinoscriptsyntax as rs
import Rhino
from copy import copy

bbox_house=house.GetBoundingBox(True)
bbox_house=bbox_house.ToBrep()

# Area of what?
area = Rhino.Geometry.AreaMassProperties.Compute(bbox_house)
# How do we find the center?
box_center = area.Centroid

# How do we get the faces of the house?
faces = house.Faces
# What types do we need? --> lists so we can add values
exploded_faces = []
not_exploded_faces = []

# What do we need to enumerate?
for i, face in enumerate( faces ):
    
    ext_face=faces.ExtractFace(i)
    not_exploded_faces.append(copy(ext_face))# saving original faces to a list for visualization
    
    area=  Rhino.Geometry.AreaMassProperties.Compute(ext_face)
    center=area.Centroid
    
    # How do we create the vector for moving a face? (tip: compare two points)
    dir = center - box_center
    
    dir.Unitize()
    dir *= 10 # distance multiplier (how far the face moves)
    
    move = Rhino.Geometry.Transform.Translation(dir) # Defining the direction in terms Rhino understands
    
    # How do we move the faces?
    ext_face.Transform(move)
    
    exploded_faces.append(ext_face) # saving exploded faces to a list for visualization
    
# What do we output?
exploded = exploded_faces
not_exploded = not_exploded_faces