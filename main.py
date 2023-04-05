import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os



i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

chan = AnalogIn(ads, ADS.P0)

found = False
count = 0
find = -1

x_vals = [30, 140, 230]
y_vals = [40, 150, 235]

vals = [[0 for j in range(3)] for i in range(3)]

for i in range(0, 3):
    for j in range(0, 3):
        os.system("echo G0 X" + str(x_vals[i]) + " Y" + str(y_vals[j]) + ">> /tmp/printer")
        vals[i][j]  = ads.read_adc()


with open("/printer_data/config/printer.cfg") as cfg:

    lines = cfg.readlines()

    for line in lines:
        if ("[bed_mesh]" in line):
            find = line
    
    if(find != -1):

        val = int(lines.index(find))
        
        newval = lines[0:val] + vals + lines [val+10:-1]

