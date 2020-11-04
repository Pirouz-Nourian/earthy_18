import numpy as np

# List of points marking the center of each district
points = _input
p = population

# http://ifcuriousthenlearn.com/blog/2015/06/18/center-of-mass/

# Create list used by ordered districts
ordered = []

# This point item refers to district 01
ordered.append(points[0])
# This point item refers to district 02
ordered.append(points[4])
# This point item refers to district 03
ordered.append(points[5])
# This point item refers to district 04
ordered.append(points[6])
# This point item refers to district 05
ordered.append(points[7])
# This point item refers to district 06
ordered.append(points[8])
# This point item refers to district 07
ordered.append(points[9])
# This point item refers to district 08
ordered.append(points[10])
# This point item refers to district 09
ordered.append(points[11])
# This point item refers to district 10
ordered.append(points[1])
# This point item refers to district 11
ordered.append(points[2])
# This point item refers to district 12
ordered.append(points[3])

# Create empty lists
x_weigt = []
y_weigt = []
z_weigt = []

# Loop trough ordered list of center points of each district
# The list of points need to be ordered from district 1 to 12 so it will be multiplied with the right population p
for i, pnt in enumerate(ordered):
    # Multiply the x, y or z value of the point with the population p of the district and place it in a list
    x_weigt.append( pnt[0]*p[i] )
    y_weigt.append( pnt[1]*p[i] )
    z_weigt.append( pnt[2]*p[i] )

# Calculate x, y or z values of center point
point_x = np.sum(x_weigt)/np.sum(p)
point_y = np.sum(y_weigt)/np.sum(p)
point_z = np.sum(z_weigt)/np.sum(p)