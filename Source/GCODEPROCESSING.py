import numpy as np

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

lookupArr = np.zeros((220, 220))

f = open("example.gcode", 'r')

lines = f.readlines()

print("started")

curZ = ""
count = 0
cont = 0
replaced = []
variable=""
initial = False

for line in lines:
    if(line == ";MESH:NONMESH\n" or line[0:5] == ";TYPE"):
        liney = lines[cont+1].split(" ")
        tmp2Z = liney[-1]
        if(tmp2Z[0] == "Z"):
            curZ = tmp2Z[1:-1]
        count += 1
        initial = True
    else:
        line = line.replace("\n", "")
        if(line.find(";") != -1):
            line = line[0:line.find(";")]
        else:
            line = line
        cont+=1

    if(cont == 4 and initial == False):
        lineys= line.split(" ")
        curZ = lineys[-1]
        initial = True
    
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
    replaced.append(line)
    
    
    
f.close()

n = open("new.gcode", 'w')


n.write("".join(replaced))

n.close()

print("Done")