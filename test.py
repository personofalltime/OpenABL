import board
import busio
import os
from ADS1115 import ADS1115


ads1115 = ADS1115()
while True :
    ads1115.set_channel()
    ads1115.config_single_ended()
    time.sleep(0.1)



i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

chan = AnalogIn(ads, ADS.P0)

print(ads1115.read_adc())

print("loading \n\n\n\n")

file = open("/printer_data/config/printer.cfg")
print(file.readlines())
