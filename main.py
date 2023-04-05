import board
import busio
import Adafruit_ADS1x15
import os

i2c = busio.I2C(board.SCL, board.SDA)
adc = Adafruit_ADS1x15.ADS1115()

found = False
count = 0
find = -1

x_vals = [30, 140, 230]
y_vals = [40, 150, 235]

vals = [[0 for j in range(3)] for i in range(3)]

for i in range(0, 3):
    for j in range(0, 3):
        os.system("echo G0 X" + str(x_vals[i]) + " Y" + str(y_vals[j]) + ">> /tmp/printer")
        vals[i][j]  = adc.read_adc(0)

print(vals)

with open("/home/pi/printer_data/config/printer.cfg") as cfg:

    lines = cfg.readlines()

    for line in lines:
        if ("points" in line):
            find = line
    
    if(find != -1):

        val = int(lines.index(find))
        
        newval = lines[0:val+1] + vals + lines [val+8:-1]

