#__author__ = "Yamuna Sakthivel (4738578)"
#__version__ = "2018.09.14"

import rhinoscriptsyntax as rs
import Rhino
from copy import copy

bbox_house = house.GetBoundingBox (True)
bbox_house = bbox_house.ToBrep()

center_of_the_box = Rhino.Geometry.AreaMassProperties.Compute(bbox_house)
centroid_box = center_of_the_box.Centroid

faces = house.Faces

exploded_faces = []
not_exploded_faces = []

for i, face in enumerate(faces):
    
    ext_face=faces.ExtractFace(i)
    not_exploded_faces.append(copy(ext_face))

    center_of_the_face = Rhino.Geometry.AreaMassProperties.Compute(ext_face)
    centroid_face = center_of_the_face.Centroid
    
    dir = centroid_face-centroid_box
    dir.Unitize()
    dir *= 10

    move = Rhino.Geometry.Transform.Translation(dir)
    ext_face.Transform(move)
    exploded_faces.append(ext_face)

exploded = exploded_faces
not_exploded = not_exploded_faces



