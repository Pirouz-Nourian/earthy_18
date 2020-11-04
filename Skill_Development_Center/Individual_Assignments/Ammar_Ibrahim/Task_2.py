import rhinoscriptsyntax as rs
import Rhino
from copy import copy

bounding_box= house.GetBoundingBox(True)
bbox_house=bounding_box.ToBrep()

area= Rhino.Geometry.AreaMassProperties.Compute(bbox_house)
bbox_center= area.Centroid

faces=house.Faces

not_exploded_faces=[]
exploded_faces=[]

for x,face in enumerate(faces):

    ext_face= faces.ExtractFace(x)
    not_exploded_faces.append(copy(ext_face))
    area= Rhino.Geometry.AreaMassProperties.Compute(ext_face)
    center= area.Centroid
    
    dir= center- bbox_center
    dir.Unitize()
    dir *= distance
    
    move= Rhino.Geometry.Transform.Translation(dir)
    ext_face.Transform(move)
    exploded_faces.append(ext_face)
    
    exploded= exploded_faces
    not_exploded= not_exploded_faces
    