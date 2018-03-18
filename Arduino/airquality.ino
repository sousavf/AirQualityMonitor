#include <MQ135.h>

MQ135 gasSensor = MQ135(0);

#define RLOAD 1.0

void setup()
{
  Serial.begin(9600);

}
void loop()
{

  float raw = gasSensor.getResistance();
  float rzero = gasSensor.getRZero();
  float ppm = gasSensor.getPPM();

  Serial.print("data");
  Serial.print(";");
  Serial.print(raw);
  Serial.print(";");
  Serial.print(rzero);
  Serial.print(";");
  Serial.print(ppm);
  Serial.print(";");
  
  Serial.println();
  delay(5000);
}