import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import random as rn


res = float(res)
board = [[0 for i in range(int(y))] for i in range(int(x))]
pals = []


# define modules
modules = []

# retreiving the length of the list of the modules
len = len(width)
id = 0
poses = []
# iterating over the list and creating modules
for mc in range(1,len):
    
    # retrieving width, depth, height and quantity for this module
    w = [-float(width[mc])/2, float(width[mc])/2]
    d = [-float(depth[mc])/2, float(depth[mc])/2]
    h = [0, float(height[mc])]
    q = int(quantity[mc])
    
    # repeating the creation process for q times which is the quantity of this module
    for qc in range(q):
        # randomizing initial position
        pos = [rn.randint(0, x),rn.randint(0, y)]
        poses.append(pos)
        # aligning initial position to board
        for ranpal in poses:
            pal = rs.CreatePoint(ranpal)
            palx = res * int(pal.X/res)
            paly = res * int(pal.Y/res)
            pal = rg.Point3d(palx + res/2, paly + res/2, 0)
            pals.append(pal)
            gridposes = pals
        # initiating the mesh
        module = rg.Mesh()
        #iterating through verticies of the box
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    #creating the point (vertex)
                    point = rg.Point3d(w[i], d[j], h[k])
                    #adding the point to the mesh as verticies
                    module.Vertices.Add(point)
                    
        #Add all faces to the mesh
        #Faces are defined counter-clockwise
        #Bottom
        module.Faces.AddFace(0,4,6,2)
        #Top
        module.Faces.AddFace(1,5,7,3)
        #Sides
        module.Faces.AddFace(0,4,5,1)
        module.Faces.AddFace(4,6,7,5)
        module.Faces.AddFace(6,2,3,7)
        module.Faces.AddFace(2,0,1,3)
        
        # adding the mesh to the list of meshes
        modules.append(module)
        
        # determing the points occupied by the module
        ws = int(float(width[mc])/(res*2))
        ds = int(float(depth[mc])/(res*2))
        
#        for gridpos in gridposes:
#            for i in range(gridpos[0]-ws, gridpos[0]+ws):
#                for j in range(d[1]-ds, d[1]+ds):
#                    board[i][j] = id
#                    id += 1

# Output the mesh you constructed


m1 = modules
pos1 = gridposes

print gridposes