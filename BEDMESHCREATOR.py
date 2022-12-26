import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

def prep(x, y, depth):
    out = [0 for l in range(depth)]
    val = (y-x)/depth
    out[0] = x
    for i in range(1, depth):
        out[i] = round(x+(val*i), 3)
    out.append(y)
    return out
    

inputDat = [[10, 5, 3], [5, 9, 6], [7, 4, 1]]

width = len(inputDat)-1
depth = len(inputDat[0])-1

subDepth = 20

xInterps = [[] for i in range(width+1)]
yInterps = [[] for i in range(depth+1)]

for i in range(0, depth+1):
    for j in range(0, width):
        xInterps[i] = xInterps[i] + prep( inputDat[i][j], inputDat[i][j+1], subDepth)


for i in range(0, depth+1):
    for j in range(0, width):
        yInterps[i] = yInterps[i] + prep( inputDat[j][i], inputDat[j+1][i], subDepth)

totArray = [[0 for x in range(2*subDepth+1)]for i in range(2*subDepth +1 )]

xInterps, yInterps = yInterps, xInterps

for j in range(0, depth+1):
    for i in range(0, width*subDepth+1):
        totArray[j*subDepth][i]  = xInterps[j][i]

for j in range(0, width+1):
    for i in range(0, depth*subDepth+1):
        totArray[i][j*subDepth] = yInterps[j][i]


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


for i in range(1, len(totArray)):
    for j in range(1, len(totArray)):
        topLeft = (math.floor(i/21)*subDepth, math.floor(j/21)*subDepth, totArray[math.floor(i/21)*subDepth][math.floor(j/21)*subDepth])
        topRight = (math.floor(i/21)*subDepth + subDepth, math.floor(j/21)*subDepth, totArray[math.floor(i/21)*subDepth + subDepth][math.floor(j/21)*subDepth])
        botLeft = (math.floor(i/21)*subDepth, math.floor(j/21)*subDepth + subDepth, totArray[math.floor(i/21)*subDepth][ math.floor(j/21)*subDepth + subDepth])
        botRight = (math.floor(i/21)*subDepth + subDepth, math.floor(j/21)*subDepth + subDepth, totArray[math.floor(i/21)*subDepth + subDepth][math.floor(j/21)*subDepth + subDepth])
        totArray[i][j] = bilinear_interpolation(i, j, [topLeft, topRight, botLeft, botRight])


z = np.asarray(totArray)
x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

v = input("3D OR 2D?")
if(v == "3"):
    di = True
else:
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