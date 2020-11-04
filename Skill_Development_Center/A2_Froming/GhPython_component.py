"""Creates bricks on a surface and places a  compass in the middle.
    
    !!!!!!!!!!!!!!!!!!!!!!!!
    !!! WORK IN PROGRESS !!!
    !!!!!!!!!!!!!!!!!!!!!!!!
    
    Inputs:
        the_shape: The surface that needs to be transformed to bricks. The surface will be the inside of the building and the bricks will be placed on the outside
        the_shape_brep: The same surface, but import it as a brep, because the script needs both. Converting it in the script will get the untrimmed surface as a Brep.
        brick_width: The width of 1 brick
        brick_length: The length of 1 brick
        brick_height: The height of 1 brick
        compass_z: Height of the centrepoint of the compass
    Output:
        out_bricks: All the bricks made by the script
        out_selected_brick: One brick where the compass is aimed at
        out_selected_brick_pnt: The centre point of this brick
        out_compass_centre: Centre point of the compass
        out_arm_length: Length of the arm for the selected brick in mm
        out_degree_inclination: Vertical angle in degrees of the arm for selected brick in mm
        out_degree_azimuth: Horizontal angle in degrees of the arm for selected brick in mm"""

__author__ = "Jeroen de Bruijn 4502019"
__version__ = "2018.10.05"



##### IMPORT

# Import Rhino Geometry libraries
import Rhino.Geometry as rg
# Import Point3dList to campare distance from one point to a list of points
from Rhino.Collections import Point3dList
# Import math functions
import math as m



##### FUNCTION

# Function to place the bricks on a curve
def placeBricks(the_curve):
    # Create empty list
    row_of_bricks = []
    
    # Get curve length
    length_curve = the_curve.GetLength()
    # Calculate the amount of half bricks that would fit on this curve
    amount = int(length_curve / halfbrick_length)
    
    # Check if the amount of points that should be created is odd
    if amount % 2 == 1:
        # Substract one to make the amount even
        amount -= 1
    
    # Check if counter is even
    if counter % 2 == 0:
        # Divide the curve in relative points on the curve, exclude both end points
        division_points = the_curve.DivideByCount(amount, False)
    else:
        # Divide the curve in relative points on the curve, include both end points
        division_points = the_curve.DivideByCount(amount, True)
    
    # Create new list
    NEW_division_points = []
    
    # Loop trough each point
    for num, p in enumerate(division_points):
        # Check if the number is even or if it is the last point
        #if num % 2 == 0 or num == len(division_points)-1:
        # Check if the number is even
        if num % 2 == 0:
            # Add the point to the list
            NEW_division_points.append(p)
    
    # Loop trough each division point
    for pnt in NEW_division_points:
        # Get XYZ point
        pnt_world = the_curve.PointAt(pnt)
        # Get tangent
        brick_tangent = the_curve.TangentAt(pnt)
        
        # Get information of the surface at that point
        surf_pnt_info = the_shape.ClosestPoint(pnt_world)
        # Get the u value of the point
        surf_u = surf_pnt_info[1]
        # Get the v value of the point
        surf_v = surf_pnt_info[2]
        
        # Get information of the surface at that u and v point
        surf_u_v_info = the_shape.Evaluate(surf_u, surf_v, 1)
        # Get the set of vectors at that point using [2]. Get the normal vector using [0]
        surf_vect = surf_u_v_info[2][1]
        
        # Clone the original brick box
        new_brick = brick.Clone()
        
        # Get movement value to move the brick to a point on the curve
        movement = pnt_world - brick.Center
        # Direction in Rhino terms
        movement = rg.Transform.Translation(movement)
        # Move the brick to the centre point
        new_brick.Transform(movement)
        
        # Get rotation value to rotate the brick to the tangent of the curve
        rotation = rg.Transform.Rotation( rg.Vector3d(0,1,0), brick_tangent, pnt_world )
        # Rotate the brick
        new_brick.Transform(rotation)
        
        # Get rotation value to rotate the vertical axis of the brick to the vector of the surface
        rotation = rg.Transform.Rotation( new_brick.Plane[3], surf_vect, pnt_world )
        # Rotate the brick
        new_brick.Transform(rotation)
        
        # Get the corners of the new brick
        corners_new_brick = new_brick.GetCorners()
        # Calculate new centre point so the brick is shifted away from surface and the bricks don't intersect
        new_centre_pnt = (corners_new_brick[1] + corners_new_brick[2])/2
        # Movement value and direction in Rhino terms
        movement = rg.Transform.Translation(new_brick.Center - new_centre_pnt)
        # Move the brick to the centre point
        new_brick.Transform(movement)
        
        # Add brick to the list which holds all the rows
        row_of_bricks.append(new_brick)
    
    # Return data
    return row_of_bricks

# Function to calculate the data for the compass
def compassOutput(pnt):
    # Calculate x, y and z values
    x_val = pnt.X - comp_centre.X
    y_val = pnt.Y - comp_centre.Y
    z_val = pnt.Z - comp_centre.Z
    
    # Calculate radius
    r = m.sqrt( m.pow(x_val,2) + m.pow(y_val,2) + m.pow(z_val,2) )
    # Calculate inclination
    incl = m.acos(z_val/r)
    # Calculate azimuth. Use atan2, because it knows in which quadrant you work
    azim = m.atan2(y_val, x_val)
    
    # Convert from radians to degrees
    degree_incl = m.degrees(incl)
    degree_azim = m.degrees(azim)
    
    # Return the data
    return r, degree_incl, degree_azim



##### MAIN CODE

# Empty list which holds lists, each list will contains a row of bricks
all_bricks = []
# Empty lists for compass data
ALL_arm_length = []
ALL_degree_inclination = []
ALL_degree_azimuth = []

# Create single brick on world xy plane. DO NOT convert it to a brep, it uses much more cpu and memory
brick = rg.Box( rg.Plane.WorldXY, rg.Interval(0, brick_width), rg.Interval(0, brick_length), rg.Interval(0, brick_height) )

# Variable for half a brick length
halfbrick_length = brick_length / 2
# Create half a brick length
brick_half = rg.Box( rg.Plane.WorldXY, rg.Interval(0, brick_width), rg.Interval(0, halfbrick_length), rg.Interval(0, brick_height) )

# Create bounding box around input surface
bbox = the_shape.GetBoundingBox(True)
# Get corners of the bounding box
bbox_corners = bbox.GetCorners()
# Get height of bounding box
bbox_height = bbox_corners[4][2]

# Convert it to brep so it is possible to get the surfaces
bbox_brep = bbox.ToBrep()
# Get the bottom surface, number 0-3 are the sided, 4 bottom, 5 top
bbox_surface_bottom = bbox_brep.Surfaces[4]
# Calculate the area
bbox_surf_area = rg.AreaMassProperties.Compute(bbox_surface_bottom)
# Get centre point
bbox_bottom_centre = bbox_surf_area.Centroid

# Place centre point of compass in the middle of the base of the shape
comp_centre = rg.Point3d(bbox_bottom_centre.X, bbox_bottom_centre.Y, compass_z)

# Use the bottom of the bounding box as the first cutting surface
cutting_surface = bbox_surface_bottom

# Create vertical vector
dirz = rg.Vector3d(0,0,1)
# Move the cutting surface a bit up to prevent wrongly placed bricks on the first curve
cutting_surface.Transform(rg.Transform.Translation(dirz * (.01)))

# Loop counter
counter = 0

# Run loop while the Z value of the centroid of the cutting surface is lower than half a brick below the top of the shape
while( rg.AreaMassProperties.Compute(cutting_surface).Centroid[2] <= bbox_height - brick_height ):
    # Intersect the shape with the cutting surface
    intersection_info = rg.Intersect.Intersection.BrepSurface(the_shape_brep, cutting_surface, 0.01)
    
    # Loop trough each part in the array of curves. Even if there is only 1 curve it is still an array of curves
    for curve_part in intersection_info[1]:
        # Run function to place bricks on the curve
        bricks_on_crv = placeBricks(curve_part)
        # Add bricks to list
        all_bricks.append(bricks_on_crv)
    
    # Get first brick in the row which is just created
    first_brick = bricks_on_crv[0]
    # Get the corners of this brick
    corners_first_brick = first_brick.GetCorners()
    # Get the height of the next curve of bircks
    next_curve_start_pnt = (corners_first_brick[5] + corners_first_brick[6])/2
    
    # Get plane of the sufrace [1] and get the centre point [0] of that plane
    surf_centre = cutting_surface.TryGetPlane()[1][0]
    
    # Distance
    distancez = dirz * (next_curve_start_pnt.Z - surf_centre.Z)
    # Direction in Rhino terms
    movez = rg.Transform.Translation(distancez)
    # Move the cutting surface up
    cutting_surface.Transform(movez)
    
    # Add up counter
    counter += 1

# TEST Choose the brick. Replace this with proper selection input, select row and brick number in Grasshopper
choosen_brick_row = 54
choosen_brick_num = 22

# Select the brick
choosen_brick = all_bricks[choosen_brick_row][choosen_brick_num]
# Call function on the centre of the selected brick to calculate compass data
ONE_arm_length, ONE_degree_inclination, ONE_degree_azimuth = compassOutput(choosen_brick.Center)

# Count all bricks
amount_of_bricks = 0

# Loop trough the whole list of rows
for row in all_bricks:
    # Get amount of birck in row
    amount_of_bricks += len(row)
    # Loop trough each brick in the row
    for brk in row:
        # Call function on the centre of the brick to calculate compass data
        arm_length, degree_inclination, degree_azimuth = compassOutput(brk.Center)
        # Add values to lists
        ALL_arm_length.append(arm_length)
        ALL_degree_inclination.append(degree_inclination)
        ALL_degree_azimuth.append(degree_azimuth)



##### OUTPUT

# All bricks
out_bricks = all_bricks
out_bricks_amount = amount_of_bricks

# The chosen brick
out_selected_brick_row = choosen_brick_row
out_selected_brick_num = choosen_brick_num
out_selected_brick = choosen_brick
out_selected_brick_pnt = choosen_brick.Center

# Centre point of the compass
out_compass_centre = comp_centre

# Compass data for the selected brick
out_arm_length = ONE_arm_length
out_degree_inclination = ONE_degree_inclination
out_degree_azimuth = ONE_degree_azimuth

# Compass data for all brick
out_all_arm_length = ALL_arm_length
out_all_inclination = ALL_degree_inclination
out_all_azimuth = ALL_degree_azimuth