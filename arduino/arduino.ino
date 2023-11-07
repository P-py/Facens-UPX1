#define pinoR1 12
#define pinoR2 7
#define pinoY1 11
#define pinoY2 8
#define pinoG1 10
#define pinoG2 9

#define DisplayPinoA 3
#define DisplayPinoB 2
#define DisplayPinoC A0
#define DisplayPinoD A1
#define DisplayPinoE A2
#define DisplayPinoF 4
#define DisplayPinoG 5

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
  pinMode(DisplayPinoA, OUTPUT);
  pinMode(DisplayPinoB, OUTPUT);
  pinMode(DisplayPinoC, OUTPUT);
  pinMode(DisplayPinoD, OUTPUT);
  pinMode(DisplayPinoE, OUTPUT);
  pinMode(DisplayPinoF, OUTPUT);
  pinMode(DisplayPinoG, OUTPUT);
  digitalWrite(pinoR1, HIGH);
  digitalWrite(pinoR2, HIGH);
}

void contagem(){
  for (int i=0; i<=9; i++){
    switch(i){
      case 0:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, HIGH);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, LOW);
        delay(1000);
        break;
      case 1:
        digitalWrite(DisplayPinoA, LOW);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, LOW);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, LOW);
        digitalWrite(DisplayPinoG, LOW);
        delay(1000);
        break;
      case 2:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, LOW);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, HIGH);
        digitalWrite(DisplayPinoF, LOW);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 3:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, LOW);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 4:
        digitalWrite(DisplayPinoA, LOW);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, LOW);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 5:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, LOW);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 6:
        digitalWrite(DisplayPinoA, LOW);
        digitalWrite(DisplayPinoB, LOW);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, HIGH);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 7:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, LOW);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, LOW);
        digitalWrite(DisplayPinoG, LOW);
        delay(1000);
        break;
      case 8:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, HIGH);
        digitalWrite(DisplayPinoE, HIGH);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, HIGH);
        delay(1000);
        break;
      case 9:
        digitalWrite(DisplayPinoA, HIGH);
        digitalWrite(DisplayPinoB, HIGH);
        digitalWrite(DisplayPinoC, HIGH);
        digitalWrite(DisplayPinoD, LOW);
        digitalWrite(DisplayPinoE, LOW);
        digitalWrite(DisplayPinoF, HIGH);
        digitalWrite(DisplayPinoG, HIGH);
        delay(2000);
        break;
    }
  }
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
    else if ((input=="R1R2"||input=="R2R1")&&(estado1=="G")){
      digitalWrite(pinoY1, HIGH);
      delay(3000);
      digitalWrite(pinoR1, HIGH);
      estado1="R";
      digitalWrite(pinoG1, LOW);
      digitalWrite(pinoY1, LOW);
    }
    else if ((input=="R1R2"||input=="R2R1")&&(estado2=="G")){
      digitalWrite(pinoY2, HIGH);
      delay(3000);
      digitalWrite(pinoR2, HIGH);
      estado2="R";
      digitalWrite(pinoG2, LOW);
      digitalWrite(pinoY2, LOW);
    }
    contagem();
  }
}
