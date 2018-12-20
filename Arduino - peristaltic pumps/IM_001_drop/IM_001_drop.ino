/* Imagination Machine 2.0 by Clara Leivas, 2018 
 * licensed under CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/4
 */


int red = 11;    
int purple = 10;
int blue = 9;

void setup() {
  Serial.begin(9600);

}

void loop() {
 //analogWrite(red, 255);
 //analogWrite(purple, 255);
 //analogWrite(blue, 255);
}

void drop(int _p){
  int p = _p;
  int a = 160;
  if(p == blue) a = 180;
  else if(p == purple) a = 160;
  analogWrite(p, a);
  delay(120);
  analogWrite(p, 0);
}

void serialEvent() {
    char inByte = (char)Serial.read();

   if(inByte == 'r') drop(red);
   else if(inByte == 'p') drop(purple);
   else if(inByte == 'b') drop(blue);
}
