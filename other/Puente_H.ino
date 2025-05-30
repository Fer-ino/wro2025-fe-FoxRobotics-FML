//Motor izquierdo
int PWMA = 19; 
int AIN2 = 18;
int AIN1 = 5;

//Activación del controlador
int STBY = 17;


void setup() {
Serial.begin(115200);
pinMode(PWMA,OUTPUT);
pinMode(AIN2,OUTPUT);
pinMode(AIN1,OUTPUT);
pinMode(STBY,OUTPUT);
digitalWrite(STBY,HIGH);
}

void loop() {
//Motor izquierdo
digitalWrite(AIN2,LOW);
digitalWrite(AIN1,HIGH);
analogWrite(PWMA,200);
Serial.println("Hola");
}
