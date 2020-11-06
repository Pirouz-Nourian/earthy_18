import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Grasshopper as gh

# cone surface
plane = rs.PlaneFromPoints([0,0,0],[1,0,0],[0,1,0])
cone = rs.AddCone(plane, -coneheight, coneradius) 

# contour curves
startpoint = [0,0,(-coneheight+(brickheight/2))]
endpoint = [0,0,0]
curves = rs.AddSrfContourCrvs(cone,(startpoint,endpoint),interval = (brickheight))

# divide curve into points
points = []
for i in range(0,curves.Count):
    if rs.CurveLength(curves[i]) > (brickwidth + brickdepth):
        amount = rs.CurveLength(curves[i]) // (brickwidth + (brickdepth / 2))
        length = rs.CurveLength(curves[i]) / amount
        division_points = rs.DivideCurveLength(curves[i], length)
        points.append(division_points)

# get planes at points on curve 
planes = []
for i in range(0,points.Count):
    for j in range(0,points[i].Count):
        param = rs.CurveClosestPoint(curves[i],points[i][j])
        normal = rs.CurveTangent(curves[i], param)
        each_plane = rs.PlaneFromNormal(points[i][j], normal)
        planes.append(each_plane)

# create vectors for brick translation
vectors = []
for i in range(0,points.Count):
    for j in range(0,points[i].Count):
        each_vector = rs.VectorCreate(brickpoint, points[i][j])
        vectors.append(each_vector)

# move bricks to points
bricks = []
for i in range(0,points.Count):
    for j in range(0,points[i].Count):
        brick_copy = rg.Transform.PlaneToPlane(brick, planes[i][j])
        bricks.append(brick_copy)


a = curves
b = points
c = bricks