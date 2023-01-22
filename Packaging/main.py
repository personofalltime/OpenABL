import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
import progressbar
import time
import regex as re

def findOffset(findX, findY, arr, val):
    offset = arr[int(findX)][int(findY)]
    val = float(val)*1000
    val += offset*1000
    val = round(int(val)/1000, 3)
    return val

def findX(line):
    line = line.split(" ")
    for i in range(0, len(line)):
        if(line[i][0] == "X"):
            return i
    return -1

def findY(line):
    line = line.split(" ")
    for i in range(0, len(line)):
        if(line[i][0] == "Y"):
            return i
    return -1

def processInitial(lines):
    curZ = ""
    count = 0
    cont = 0
    replaced = []
    variable=""
    initial = False

    for line in lines:
        if(line == ";MESH:NONMESH\n"):

            liney = lines[cont+1].split(" ")
            tmp2Z = liney[-1]
            if(tmp2Z[0] == "Z"):
                curZ = tmp2Z[1:-1]
            print(curZ)
            initial = True
        else:
            line = line.replace("\n", "")
            if(line.find(";") != -1):
                line = line[0:line.find(";")]
            else:
                line = line

        if(cont == 4 and initial == False):
            lineys= line.split(" ")
            curZ = lineys[-1]
            initial = True
        
        if(len(line) > 0):
            if(line[0] == "G" and (line[1] == "1" or line[1] == "0")):
                lineLst = line.split(" ")
                try:
                    xVal = findX(line)
                    yVal = findY(line)
                    if(xVal != -1 and yVal != -1):
                        x = lineLst[xVal][1:-1]
                        y = lineLst[yVal][1:-1]
                        try:
                            x = float(x)
                            y = float(y)
                            tmpZ = findOffset(x, y, lookupArr, curZ)
                            line = line[0:-2]
                            line = line + " " + "Z" + str(tmpZ) 
                        except ValueError:
                            line +=  "\n"
                except IndexError:
                    line +=  "\n"
                else:
                    line +=  "\n"
            if(line[-1] != "\n"):
                line += "\n"
        cont+=1
        replaced.append(line)
    
    return replaced

def prep(x, y, depth):
    out = [0 for l in range(depth)]
    val = (y-x)/depth
    out[0] = x
    for i in range(1, depth):
        out[i] = round(x+(val*i), 3)
    out.append(y)
    return out
    
def bilinear_interpolation(x, y, points):
        points = sorted(points)               # order points by x, then by y
        (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points
        
        if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
            raise ValueError('points do not form a rectangle')
        if not x1 <= x <= x2 or not y1 <= y <= y2:
            raise ValueError('(x, y) not within the rectangle')
        #returns the value of the position
        return round((q11 * (x2 - x) * (y2 - y) +
                q21 * (x - x1) * (y2 - y) +
                q12 * (x2 - x) * (y - y1) +
                q22 * (x - x1) * (y - y1)
            ) / ((x2 - x1) * (y2 - y1) + 0.0), 2)

def process(xInterps, yInterps, inputDat, subDepth, width, depth, divDepth, totArray):
    for i in range(0, depth+1):
        for j in range(0, width):
            xInterps[i] = xInterps[i] + prep( inputDat[i][j], inputDat[i][j+1], subDepth)


    for i in range(0, depth+1):
        for j in range(0, width):
            yInterps[i] = yInterps[i] + prep( inputDat[j][i], inputDat[j+1][i], subDepth)

    xInterps, yInterps = yInterps, xInterps

    for j in range(0, depth+1):
        for i in range(0, width*subDepth+1):
            totArray[j*subDepth][i]  = xInterps[j][i]

    for j in range(0, width+1):
        for i in range(0, depth*subDepth+1):
            totArray[i][j*subDepth] = yInterps[j][i]


    total_steps = 484000
    sub = 2200
    print("\nProcessing beginning..... \n")
    bar = progressbar.ProgressBar().start()
    for i in range(1, len(totArray)):
        for j in range(1, len(totArray)):
            #Gets the 'coordinates' of the bounding box that each value in the array is in, so that it can be used to bi-linearly interpolate
            topLeft = (math.floor(i/divDepth)*subDepth, math.floor(j/divDepth)*subDepth, totArray[math.floor(i/divDepth)*subDepth][math.floor(j/divDepth)*subDepth])
            topRight = (math.floor(i/divDepth)*subDepth + subDepth, math.floor(j/divDepth)*subDepth, totArray[math.floor(i/divDepth)*subDepth + subDepth][math.floor(j/divDepth)*subDepth])
            botLeft = (math.floor(i/divDepth)*subDepth, math.floor(j/divDepth)*subDepth + subDepth, totArray[math.floor(i/divDepth)*subDepth][ math.floor(j/divDepth)*subDepth + subDepth])
            botRight = (math.floor(i/divDepth)*subDepth + subDepth, math.floor(j/divDepth)*subDepth + subDepth, totArray[math.floor(i/divDepth)*subDepth + subDepth][math.floor(j/divDepth)*subDepth + subDepth])
            totArray[i][j] = bilinear_interpolation(i, j, [topLeft, topRight, botLeft, botRight])
            bar.update((j+(sub*(i-1)))/total_steps)
    bar.finish()
    print("\nProcessing complete! \n")

    z = np.asarray(totArray)
    return z

print("\nWelcome to the Desktop Automatic Bed Levelling  tool")
time.sleep(1)
name = input("\nPlease enter the desired GCode file's name (including extension): \t")

inp = input("Would you like a 3D OR 2D representation of the bed? ('3' & '2' respectively)")

inputDat = [[0 for x in range(3)] for y in range(3)]

file = open("input.dat", 'r')

lines = file.readlines()
print(len(lines))
for i in range(0, len(lines)):
    if(lines[i].find("\n") != -1):
        lines[i] = lines[i][0:lines[i].find("\n")]
    lines[i] = float(lines[i])
    inputDat[math.floor(i/3)][i%3] = float(lines[i])


width = len(inputDat)-1
depth = len(inputDat[0])-1

subDepth = 1100 #Ender 3 build volume (base) divided by two - adjust this as you need
divDepth = subDepth+1 #To set the quadrants for the array

xInterps = [[] for i in range(width+1)]
yInterps = [[] for i in range(depth+1)]

totArray = [[0 for x in range(2*subDepth+1)]for i in range(2*subDepth +1 )]

bed = process(xInterps, yInterps, inputDat, subDepth, width, depth, divDepth, totArray)
x, y = np.meshgrid(range(bed.shape[0]), range(bed.shape[1]))

#VISUAL REPRESENTATION OF PROCESSED DATA, AS 2D HEATMAP OR 3D GRAPH


if(inp == "3"):
    rep = True
else:
    rep = False

if(rep):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, bed)
    plt.title('3-Dimensional height map of the printer bed (0,0 is origin)')
    plt.show()
else:
    plt.figure()
    plt.title('2-Dimensional height map of the printer bed (top left is origin)')
    p = plt.imshow(bed)
    plt.colorbar(p)
    plt.show()

lookupArr = bed
f = open(name, 'r')
lines = f.readlines()
replaced = processInitial(lines)
f.close()
print("Writing to file....")
n = open("new.gcode", 'w')
n.write("".join(replaced))
n.close()
print("Gcode manipulation completed - Modified file saved as " + name + "\n")

time.sleep(1)
print("Program shutting down...")
time.sleep(10)


