import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# define brick
brick = rg.Mesh()

# define the basic coordinates of the cube
point0 = rg.Point3d(0,0,0)
point1 = rg.Point3d(brickwidth,0,0)
point2 = rg.Point3d(brickwidth,brickdepth,0)
point3 = rg.Point3d(0,brickdepth,0)
point4 = rg.Point3d(0,0,brickheight)
point5 = rg.Point3d(brickwidth,0,brickheight)
point6 = rg.Point3d(brickwidth,brickdepth,brickheight)
point7 = rg.Point3d(0,brickdepth,brickheight)

# add all points to the mesh
points = [point0,point1,point2,point3,point4,point5,point6,point7]

# define a new list for the output points
outputpoints = []

# loop through what?
for point in points:
    outputpoints.append(point)
    brick.Vertices.Add(point)

# add all faces to the mesh
# faces are defined counter-clockwise
# bottom
brick.Faces.AddFace(0,1,2,3)
# top
brick.Faces.AddFace(4,5,6,7)
# sides
brick.Faces.AddFace(0,1,5,4)
brick.Faces.AddFace(1,2,6,5)
brick.Faces.AddFace(2,3,7,6)
brick.Faces.AddFace(3,0,4,7)

# output the mesh you constructed
mesh_output = brick

# create vector for brick orientation
point_a = rg.Point3d(0,(brickdepth/2),(brickheight/2))
point_b = rg.Point3d(brickwidth,(brickdepth/2),(brickheight/2))
point_c = rg.Point3d((brickwidth/2),(brickdepth/2),(brickheight/2))
brickvector = rs.VectorCreate(point_a, point_b)

# get plane at center point 
brickplane = rs.PlaneFromNormal(point_c, brickvector)

brickpoint = point_c

