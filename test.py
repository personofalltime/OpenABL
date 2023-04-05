import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os



i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

chan = AnalogIn(ads, ADS.P0)

print(ads.read_adc())

print("loading \n\n\n\n")

file = open("/printer_data/config/printer.cfg")
print(file.readlines)
