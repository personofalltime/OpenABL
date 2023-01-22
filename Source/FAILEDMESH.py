import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter

#DOES NOT WORK - DO NOT USE

depthToSubdivide = 22
depth = 3
width = 3

BedLevellingData = [[10, 5, 10], [10, 5, 8], [10, 5, 9]]
outputX = [[] for y in range(width)] 
outputY = [[] for x in range(depth)]

totX = []
totY = []

totOutput = [[0 for l in range(width*depthToSubdivide)] for n in range(depth*depthToSubdivide)]



def prep(x, y, depth):
    out = [0 for l in range(depth)]
    val = (y-x)/depth
    out[0] = x
    for i in range(1, depth):
        out[i] = round(x+(val*i), 3)
    out.append(y)
    return out
    


for i in range(0, depth):
    for j in range(0, width-1):
        outputX[i] = outputX[i] + prep( BedLevellingData[i][j], BedLevellingData[i][j+1], depthToSubdivide)


for i in range(0, depth):
    for j in range(0, width-1):
        outputY[i] = outputY[i] + prep( BedLevellingData[j][i], BedLevellingData[j+1][i], depthToSubdivide)

print(len(outputY[0]))

for j in range(0, depth+1):
    for k in range(0, depth):
        for i in range(0, (depthToSubdivide)*2):
            totOutput[depthToSubdivide*j-1][int(i/2)+(k*depthToSubdivide)] = outputX[k][i]


for j in range(0, depth+1):
    for k in range(0, depth):
        for i in range(0, (depthToSubdivide)*2):
            totOutput[int(i/2)+(k*depthToSubdivide)-1][depthToSubdivide*j-2] = outputY[k][i]
            totOutput[int(i/2)+(k*depthToSubdivide)-1][depthToSubdivide*j-2] = outputY[k][i]
            totOutput[int(i/2)+(k*depthToSubdivide)-2][depthToSubdivide*j-1] = outputY[k][i]
            totOutput[int(i/2)+(k*depthToSubdivide)-1][depthToSubdivide*j-2] = outputY[k][i]

#First option in array is column of table, second is the row

def bilinear_interpolation(x, y, points):
    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points
    
    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return round((q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0), 2)

count = len(totOutput)

count = len(totOutput)

for i in range(0, depthToSubdivide*width):
    for j in range(0, depthToSubdivide*width):
        
        n = 22*math.ceil(j/22)-1
        m = 22*math.ceil(i/22)-1

        p1 = (n-21, m-21, totOutput[n-21][m-21])
        p2 = (n, m-21, totOutput[n][m-21])
        p3 = (n-21, m, totOutput[n-21][m])
        p4 = (n, m, totOutput[n][m])

        totOutput[j-1][i-1] = bilinear_interpolation(j-1, i-1, [p1, p2, p3, p4])



#totOutput = gaussian_filter(totOutput, sigma=7)

z = np.asarray(totOutput)
x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

di = False

if(di):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z)
    plt.title('z as 3d height map')
    plt.show()
else:
    plt.figure()
    plt.title('z as 2d heat map')
    p = plt.imshow(z)
    plt.colorbar(p)
    plt.show()