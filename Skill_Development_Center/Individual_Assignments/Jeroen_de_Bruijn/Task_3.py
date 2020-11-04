"""Provides a scripting component.
    Inputs:
        cone_diameter: diameter of the cone! So NOT the radius (diameter cone = length bbox = width bbox)
        cone_length: height of the cone
    Output:
        out: error catcher
        out_cone: brep of cone
        out_bounding box: brep of bounding box around cone

FUTURE IMPROVEMENTS:
The way the voxel list is created should be made much more efficient.
- It could be done with a better loop, so one instance is being shallow duplicated all the time.
- Maybe it is also better to first define a grid of points and then duplicate shallow mutliple voxels to these points
- Maybe the voxolisation process could be accomplished using rasterworks.dll
- Coloring can be done inside python instead of GH

The script is quite slow when voxel_size is set to 1, therefore it is set to 2
"""

# Voxel define size
voxel_size = 2 # Should be 1, but set to 2 in order to decrease processing time

__author__ = "Jeroen de Bruijn 4502019"
__version__ = "2018.09.05"

import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg

# Create plane at top of cone facing down, because apex of the cone is at the plane's origin
center_point = rg.Point3d(0, 0, cone_length)
height_point = rg.Point3d(0, 0, 0)
zaxis = height_point - center_point
conePlane = rg.Plane(center_point, zaxis)

# Create cone
cone = rg.Cone(conePlane, cone_length, cone_diameter / 2)
cone = cone.ToBrep(True)
# Get cone volume
cone_volume = rg.VolumeMassProperties.Compute(cone)
# Cone centroid
cone_center = cone_volume.Centroid

# Create bounding box around cone
bbox_cone = cone.GetBoundingBox(True)
# bbox_cone = bbox_cone.ToBrep()
bbox_corners = bbox_cone.GetCorners()



# Create intervals to position first voxel on corner 0 of the bounding box
voxel_interval_x = rg.Interval(bbox_corners[0][0], bbox_corners[0][0] + voxel_size)
voxel_interval_y = rg.Interval(bbox_corners[0][1], bbox_corners[0][1] + voxel_size)
voxel_interval_z = rg.Interval(bbox_corners[0][2], bbox_corners[0][2] + voxel_size)
# Create single voxel on world xy plane and equal in size over every axis
voxel = rg.Box(rg.Plane.WorldXY, voxel_interval_x, voxel_interval_y, voxel_interval_z)
# Transform to Brep
voxelbrep = voxel.ToBrep()



# Voxels listx
voxels_x = []

# Vector for moving a voxel over the x-axis
dirx = bbox_corners[1] - bbox_corners[0]
dirx.Unitize()
# Distance multiplier
dirx *= voxel_size
# Direction in Rhino terms
movex = rg.Transform.Translation(dirx)

# Loop trough range which has the size of the amount of voxels needed
for i in range(int((bbox_corners[1][0] - bbox_corners[0][0])/voxel_size)):
    # Add voxel to list
    voxels_x.append(voxelbrep)
    # GeometryBase.DuplicateShallow Method: Constructs a light copy of this object. By "light", it is meant that the same underlying data is used until something is done to attempt to change it. For example, you could have a shallow copy of a very heavy mesh object and the same underlying data will be used when doing things like inspecting the number of faces on the mesh. If you modify the location of one of the mesh vertices, the shallow copy will create a full duplicate of the underlying mesh data and the shallow copy will become a deep copy.
    # Shallow duplicate of the voxel (I think this uses less memory/cpu?)
    voxelbrep = rg.GeometryBase.DuplicateShallow(voxelbrep)
    # Move the voxel
    voxelbrep.Transform(movex)



# Voxels list 2D
voxels_2d = []

# Vector for moving a voxel over the y-axis
diry = bbox_corners[2] - bbox_corners[1]
diry.Unitize()

# Loop trough range which has the size of the amount of voxels needed
for i in range(int((bbox_corners[2][1] - bbox_corners[1][1])/voxel_size)):
    # Distance multiplier
    new_diry = diry * voxel_size * i
    # Direction in Rhino terms
    movey = rg.Transform.Translation(new_diry)
    # Loop trough all the x-axis voxels
    for voxel in voxels_x:
        voxel = rg.GeometryBase.DuplicateShallow(voxel)
        # Move the x-axis voxels over the y-axis
        voxel.Transform(movey)
        # Add voxel to list
        voxels_2d.append(voxel)



# Voxels list 3D
voxels_3d = []

# Vector for moving a voxel over the z-axis
dirz = bbox_corners[4] - bbox_corners[0]
dirz.Unitize()

# Loop trough range which has the size of the amount of voxels needed
for i in range(int((bbox_corners[4][2] - bbox_corners[0][2])/voxel_size)):
    # Distance multiplier
    new_dirz = dirz * voxel_size * i
    # Direction in Rhino terms
    movez = rg.Transform.Translation(new_dirz)
    # Loop trough all the 2d voxels
    for voxel in voxels_2d:
        voxel = rg.GeometryBase.DuplicateShallow(voxel)
        # Move the 2D voxels over the z-axis
        voxel.Transform(movez)
        # Add voxel to list
        voxels_3d.append(voxel)

# List to store lengths
length = []

# Loop trough all the voxels
for voxel in voxels_3d:
    # Area
    area = rg.AreaMassProperties.Compute(voxel)
    # Center
    voxel_center = area.Centroid
    
    # Find closest point on surface of cone from center of voxel
    closestPoint = rg.Brep.ClosestPoint(cone, voxel_center)
    # Draw a line from the voxel center to the closest point
    line = rg.Line(voxel_center, closestPoint)
    
    # Check if voxel center is inside the cone
    if cone.IsPointInside(voxel_center, Rhino.RhinoMath.SqrtEpsilon, True):
        # Set var positive
        insideCone = 1
    else:
        # Set var negative
        insideCone = -1
    
    # Make distance negative or positive
    distance = line.Length * insideCone
    # Add distance to list
    length.append(distance)

# Brep of the cone
out_cone = cone
# List of all voxels
out_LIST_voxels = voxels_3d
# List of all lenghts
out_LIST_lengths = length
# Output the longest negative length
out_length_lowest = min(length)
# Set output of the highest value to 0 instead of 'max(length)', because everythin above 0 is inside the cone
out_length_highest = 0
# Completion message
print("Script completed")