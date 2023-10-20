#define pinoR1 12
#define pinoR2 7
#define pinoY1 11
#define pinoY2 8
#define pinoG1 10
#define pinoG2 9

String estado1="R";
String estado2="G";

void setup() {
  Serial.begin(9600);
  pinMode(pinoR1, OUTPUT);
  pinMode(pinoR2, OUTPUT);
  pinMode(pinoY1, OUTPUT);
  pinMode(pinoY2, OUTPUT);
  pinMode(pinoG1, OUTPUT);
  pinMode(pinoG2, OUTPUT);
  digitalWrite(pinoR1, HIGH);
  digitalWrite(pinoG2, HIGH);
}

void loop() {
  if (Serial.available()>0){
    String input = Serial.readString();
    if (input=="G1R2"&&estado1=="R"){
      digitalWrite(pinoY2, HIGH);
      delay(3000);
      digitalWrite(pinoR2, HIGH);
      estado2="R";
      digitalWrite(pinoG2, LOW);
      digitalWrite(pinoY2, LOW);
      digitalWrite(pinoG1, HIGH);
      estado1="G";
      digitalWrite(pinoR1, LOW);
    }
    else if (input=="R1G2"&&estado2=="R"){
      digitalWrite(pinoY1, HIGH);
      delay(3000);
      digitalWrite(pinoR1, HIGH);
      estado1="R";
      digitalWrite(pinoG1, LOW);
      digitalWrite(pinoY1, LOW);
      digitalWrite(pinoG2, HIGH);
      estado2="G";
      digitalWrite(pinoR2, LOW);
    }
  }
}
