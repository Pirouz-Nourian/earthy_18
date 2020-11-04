"""Explodes the piglet's house
    Inputs:
        house: the piglet's house brep
    Output:
        exploded: exploded faces
        not_exploded: not exploded faces"""

__author__ = "Mr. Wolf"
__version__ = "2018.09.04"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
from copy import copy


bbox_house=house.GetBoundingBox(True)
bbox_house=bbox_house.ToBrep()  

# Area of what?
area = rg.AreaMassProperties.Compute(bbox_house)

# How do we find the center?
box_center = area.Centroid
print(box_center)
print(box_center)
# How do we get the faces of the house?
faces = house.Faces
print(house)
# What types do we need?
exploded_faces = []
not_exploded_faces = []

# What do we need to enumerate?
for i, sadface in enumerate( faces ):
    print(i, sadface)
    
    ext_face=faces.ExtractFace(i)
    #print(i , ext_face)
    not_exploded_faces.append(copy(ext_face))# saving original faces to a list for visualization
    #print(not_exploded_faces)
    area=  rg.AreaMassProperties.Compute(ext_face)
    center=area.Centroid
    
    # How do we create the vector for moving a face? (tip: compare two points)
    direction = center - box_center
    #print(direction)
    #print(box_center)
   
    
    #print(direction)
    direction = direction * Distance # distance multiplier (how far the face moves)
    #print(direction)
    move = rg.Transform.Translation(direction) # Defining the direction in terms Rhino understands
    
    # How do we move the faces?
    ext_face.Transform(move)
    
    exploded_faces.append(ext_face) # saving exploded faces to a list for visualization
    
# What do we output?
exploded = exploded_faces
not_exploded = not_exploded_faces