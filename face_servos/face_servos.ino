#define xMkr  65
#define yMkr  66

#include <Servo.h>

Servo xservo;
Servo yservo;

int xVal;
int yVal;

void setup()
{
  xservo.attach(10);
  yservo.attach(6);
  
  xservo.write(90);
  yservo.write(50);
  
  Serial.begin(115200);
}

void loop()
{
  if(Serial.available() > 0)
  {
    char inByte = Serial.read();
    if (inByte == xMkr)
    {
      delay(10);
      if(Serial.available() > 0)
      {
      xVal = Serial.read();
      xservo.write(xVal);
      //Serial.print("x:");
      //Serial.println(xVal);
      }
    }
    if (inByte == yMkr)
    {
      delay(10);
      if(Serial.available() > 0)
      {
      yVal = Serial.read();
      yservo.write(yVal);
      //Serial.print("y:");
      //Serial.println(yVal);
      }
    }
  }
}
