"""Provides a scripting component.
    Inputs:
        the_shape: The surface or surfaces that need to be transformed to bricks, the bricks don't stick out at the edges of the surface
        brick_width: The width of 1 brick
        brick_length: The length of 1 brick
        brick_height: The height of 1 brick
    Output:
        out_bricks: All bricks made by the script"""

"""Possible future updates:
    Add different brick bond functions. Maybe a system as per Koen his presentation of 2018-09-04"""

__author__ = "Jeroen de Bruijn 4502019"
__version__ = "2018.09.09"

import Rhino.Geometry as rg
import Rhino

# Used to round up
import math

# Used to call grashooper components
import ghpythonlib.components as ghcomp

def placeBricksStretcherBond(the_line):
    # Calculate the amount of half bricks on this line. Devide the line by the diagonal of half a brick, this ensures the bricks don't intersect
    #amount = int(the_line.GetLength() / ( (((brick_width/2) ** 2) + ((brick_length/2) ** 2))**(.5) ) )
    amount = math.ceil( ( the_line.GetLength() / ( (((brick_width/2) ** 2) + ((brick_length/2) ** 2))**(.5)) ) / 2.) * 2
    # Divide the line in relative points on the curve and add both end points
    division_points = the_line.DivideByCount(amount, True)
    
    # Check if any points exist on the line, sometimes it doesn't because the line is to small and it causes an error
    if division_points is not None:
        # Check if the counter is odd
        if counter % 2 == 1:
            # Create variable
            create_half_brick = True
        else:
            # Create variable
            create_half_brick = False
        
        # Loop trough each division point
        for i, pnt in enumerate(division_points):
            # Skip starting poiint of line to prevent bricks sticking out
            if i == 0:
                # Skip this cycle of the loop
                continue
            
            # Create variable for brick
            brick_type = brick_brep
            
            # Check if it is not the first or last run of the loop
            if i > 1:
                # Check if it is the last point of the line and if half a brick was created
                if create_half_brick and i == len(division_points) - 1:
                    # Create variable to finish the line with half a brick
                    brick_type = brick_half
                # Check if the number is odd and if a half brick was created
                elif i % 2 == 1 and create_half_brick:
                    # Skip this cycle of the loop
                    continue
                # Check if the number is even and if a half brick was not created
                elif i % 2 == 0 and create_half_brick == False:
                    # Skip this cycle of the loop
                    continue
            # Check if half a brick needs to be created
            elif create_half_brick:
                # Create variable
                brick_type = brick_half
            else:
                # Create variable
                brick_type = brick_brep
            
            # Get XYZ point
            pnt_world = the_line.PointAt(pnt)
            # Get tangent
            brick_tangent = the_line.TangentAt(pnt)
            
            # GeometryBase.DuplicateShallow Method: Constructs a light copy of this object. By "light", it is meant that the same underlying data is used until something is done to attempt to change it. For example, you could have a shallow copy of a very heavy mesh object and the same underlying data will be used when doing things like inspecting the number of faces on the mesh. If you modify the location of one of the mesh vertices, the shallow copy will create a full duplicate of the underlying mesh data and the shallow copy will become a deep copy.
            # Shallow duplicate of the brick (I think this uses less memory/cpu?)
            new_brick = rg.GeometryBase.DuplicateShallow(brick_type)
            
            # Get movement value
            movement = pnt_world - brick.Center
            # Direction in Rhino terms
            movement = rg.Transform.Translation(movement)
            # Move the brick to the point
            new_brick.Transform(movement)
            
            # Get rotation value
            rotation = rg.Transform.Rotation( rg.Vector3d(0,1,0), brick_tangent, pnt_world )
            # Rotate the brick
            new_brick.Transform(rotation)
            
            # Add brick to list
            all_bricks.append(new_brick)

# Create single brick on world xy plane
brick = rg.Box( rg.Plane.WorldXY, rg.Interval(0, brick_width), rg.Interval(0, brick_length), rg.Interval(0, brick_height) )
# Generate brep
brick_brep = brick.ToBrep()
# Variable for half a brick length
halfbrick_length = brick_length / 2
# Create half a brick length
brick_half = rg.Box( rg.Plane.WorldXY, rg.Interval(0, brick_width), rg.Interval(0, halfbrick_length), rg.Interval(0, brick_height) )
# Generate brep
brick_half = brick_half.ToBrep()

# Create vector
dirz = rg.Vector3d(0,0,1)
# Distance
distancez = dirz * brick_height
# Direction in Rhino terms
movez = rg.Transform.Translation(distancez)

# Call grasshopper component Plane Trough Shape
cutting_plane = ghcomp.PlaneThroughShape(rg.Plane.WorldXY, the_shape, 10)
# Direction in Rhino terms to move the initial cutting plane up half the hight of the brick because the center of each brick will be positioned on the line
movez_half = rg.Transform.Translation(dirz * (brick_height / 2))
# Move cutting plane up
cutting_plane.Transform(movez_half)

# Create empty list
all_bricks = []

# Create bounding box around shape
bbox_shape = the_shape.GetBoundingBox(True)
# Get corners of bounding box
bbox_corners = bbox_shape.GetCorners()

# Create counter variable to keep track of amount of lines
counter = 0

# Run loop while the Z value of the centroid of the cutting plane is lower than - .01 of the top of the shape
while rg.AreaMassProperties.Compute(cutting_plane).Centroid[2] < bbox_corners[4][2] - .01:
    # Call grasshopper component Plane Trough Shape. Added [0] to only get first object, which is the line.
    # Normally a second object [1] is returned as well which contains the points ([1] is empty in this case and causes errors)
    brick_line = ghcomp.BrepXPlane(the_shape, cutting_plane)[0]
    
    # Check if brick_line is a list, if it is the case the line consists out of multiple parts
    if isinstance(brick_line, list):
        # Loop trough each part of the line
        for line_part in brick_line:
            print "test02"
            # Run function to place bricks on the line
            placeBricksStretcherBond(line_part)
    else:
        #print "test01"
        # Run function to place bricks on the line
        placeBricksStretcherBond(brick_line)
    
    # Count up
    counter = counter + 1
    # Move cutting plane up
    cutting_plane.Transform(movez)

# Output
out_bricks = all_bricks