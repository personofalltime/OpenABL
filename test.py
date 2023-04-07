import moonrakerpy as moonpy

printer = moonpy.MoonrakerPrinter('http://192.168.1.226')

printer.send_gcode("G28")
