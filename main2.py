def findLargestBeforeN(n):
  cur = 1
  cur2 = 1
  found = False
  while(found != True):
    tmp = cur+cur2
    cur=cur2
    cur2 = tmp
    if(cur2 > n):
      return cur
    elif(cur2 == n):
      return n
      
def calculate(fond, vales, n, ninit):
  while(fond == False):
    vales.append(findLargestBeforeN(n))
    if(sum(vales) == ninit):
      break
    else:
      n = n - findLargestBeforeN(n)
  return vales

def sum(lst):
  tot = 0
  for i in range(0, len(lst)):
    tot += lst[i]
  return tot

def contains(srch, lst):
    for i in range(0, len(lst)):
        if(lst[i] == srch):
            return True
    return False


n = int(input(""))
ninit = n

vales = []

fond = False

cont = 0

import progressbar

print("started")
for i in range(5000000001, 1000000000, -1):
    vales = []
    vales = calculate(fond, vales, i, i)
    if(contains(701408733,vales) == False):
        cont+=1

    print(cont)




print(cont)

for i in range(0, len(vales)):
  print(str(vales[i]) + "\t", end="")