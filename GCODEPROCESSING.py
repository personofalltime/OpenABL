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

lookupArr = np.ones((220, 220), like=None)

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
    cont+=1
    if(cont == 4 and initial == False):
            lineys= line.split(" ")
            curZ = lineys[-1]
            intial = True
   
    if(line == ";MESH:NONMESH\n" or line[0:5] == ";TYPE"):
        liney = lines[cont].split(" ")
        tmp2Z = liney[-1]
        print(liney[-1])
        if(tmp2Z[0] == "Z"):
            curZ = tmp2Z[1:-1]
        count += 1
        replaced.append(line)

    if(line[0:2] == "G1" or line[0:2] == "G0"):
        line = line.replace("\n", "")
        line = line[0:line.find(";")]
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
                    line = line + " " + "Z" + str(tmpZ) + "\n"
                    replaced.append(line)
                except ValueError:
                    line +=  "\n"
                    replaced.append(line)

        except IndexError:
            line +=  "\n"
            replaced.append(line)

        else:
            line +=  "\n"
            replaced.append(line)
    else:
        replaced.append(line)
    
    
    
f.close()

n = open("new.gcode", 'w')


n.write("".join(replaced))

n.close()

print("Done")