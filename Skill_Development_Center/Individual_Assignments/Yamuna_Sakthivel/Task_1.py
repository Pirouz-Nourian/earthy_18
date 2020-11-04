#__author__ = "Yamuna Sakthivel (4738578)"
#__version__ = "2018.09.14"

#importing rhinoscript library in order to code in rhino framework
import rhinoscriptsyntax as rs

#importing Rhino.Geometry library in order to deal with geometries in rhino
import Rhino.Geometry as rg

# Make a new mesh object called "meshobject"
meshobject = rg.Mesh()

#Define the basic coordinates of the cube
point0 = rg.Point3d(0,0,0)
point1 = rg.Point3d(1,0,0)
point2 = rg.Point3d(1,1,0)
point3 = rg.Point3d(0,1,0)
point4 = rg.Point3d(0,0,1)
point5 = rg.Point3d(1,0,1)
point6 = rg.Point3d(1,1,1)
point7 = rg.Point3d(0,1,1)

#Add all points to the mesh
points = [point0,point1,point2,point3,point4,point5,point6,point7]

#Define a new list for the output points
outputpoints = []

# Loop through what?
for point in points :
    point = point*scale + transformation
    outputpoints.append(point)
    meshobject.Vertices.Add(point)

#Add all faces to the mesh
#Faces are defined counter-clockwise
#Bottom
meshobject.Faces.AddFace(0,1,2,3)
#Top
meshobject.Faces.AddFace(4,5,6,7)
#Sides
meshobject.Faces.AddFace(0,1,5,4)
meshobject.Faces.AddFace(1,2,6,5)
meshobject.Faces.AddFace(2,3,7,6)
meshobject.Faces.AddFace(3,0,4,7)

# Output the mesh you constructed
mesh_output = meshobject