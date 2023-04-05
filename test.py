import board
import busio
from Adafruit_ADS1x15 import ADS1x15
import os



i2c = busio.I2C(board.SCL, board.SDA)
adc = Adafruit_ADS1x15.ADS1115()



print(adc.read_adc())

print("loading \n\n\n\n")

file = open("/printer_data/config/printer.cfg")
print(file.readlines)
