 #include <math.h>
 #include "NintendoExtensionCtrl.h"
#include <SdFat.h>

const int chipSelect = 10;

SdFat sd;
SdFile myFile;

Nunchuk n;

float distance; //may cause floating point errors - will check later

const float outVolt = 5.0;

float readDistance(){

  unsigned long voltage_average=0;
  double newVolt;

  for(int j = 0; j < 10; j++){
    for(int i=0; i < 64; i++){

      voltage_average += analogRead(A0);
    }
  }
  newVolt = (voltage_average >> 3) / 10;
  newVolt = newVolt * (5.0/8191);
  Serial.println(voltage_average);
  distance = 5.2819 * pow(newVolt , -1.161);
  return distance*10; //return value in  milimeters, as the gcode uses mm
}

void setup() {
  Serial.begin(9600);
  delay(400);
  
  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) sd.initErrorHalt();

  if (!myFile.open("input.dat", O_READ | O_WRITE | O_CREAT | O_APPEND )) {
    sd.errorHalt("opening test.txt for write failed");
  }

  myFile.close();

  if (!myFile.open("input.dat", O_READ | O_WRITE | O_CREAT | O_APPEND)) {
    sd.errorHalt("opening test.txt for read failed");
  }

  n.begin();
  
  while (!n.connect()) {
    Serial.println("couldn't connect");
    delay(1000);
  }

  sd.remove("input.dat");

}

void loop() {

  myFile.open("input.dat", O_READ | O_WRITE | O_CREAT | O_APPEND);
  
  bool success = n.update();
  //int joyY = n.joyY();
  //int joyX = n.joyX();
  bool zButton = n.buttonZ();

  //Commented out lines could be useful for adding extra functionality in future, using more controls
  //int accelX = n.accelX();
  //int accelY = n.accelY();
  //int accelZ = n.accelZ();

  if(zButton){
    float val = readDistance();
    myFile.println(44.05-val);//applying offsets of sensor to nozzle (36.649mm) and the nozzle-to-bed distance (0.1mm) to the value obtained
    Serial.println(44.05-val);
    myFile.close();
    delay(500);
  }
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
}