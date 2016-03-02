#include <SoftwareSerial.h>

#define LCDBAUDS 9600
#define USBBAUDS 9600
//#define USBBAUDS 38400

SoftwareSerial lcds[] = { SoftwareSerial( 2, 3 ), SoftwareSerial( 4, 5 ), SoftwareSerial( 6, 7 ), SoftwareSerial( 8, 9 ), SoftwareSerial( 10, 11 ), SoftwareSerial( 12, 13 ) };
int i;
String line1 = "1234567890123456";
String line2 = "www.mikrotron.hr";

void setup()
{
  for (i=0; i< 6; i++ ) {
    lcds[i].begin(LCDBAUDS);
  }
  delay(1000);
  bootScreen();
  Serial.begin( USBBAUDS );
}

void bootScreen() {
  for ( i=0; i<6; i++ ) {
    String msg = "e-Polica - LCD ";
    msg = msg + (i + 1);
    print( lcds[i], msg, line2 );
  }
}

byte readOne() {
  while ( !Serial.available() ) {
  }
  return Serial.read();
}
void loop() {
  while ( readOne() != '0' ) {}
  int lcd = readOne();
  if ( lcd == '0' ) {
    // status request
    Serial.write('O');Serial.write('K');
  } else {
    if ( lcd >= 48 ) lcd = lcd - '0'; // ascii zero
    for ( i = 0; i < 16; i++ ) {
      line1[i] = readOne();
    }
    for ( i = 0; i < 16; i++ ) {
      line2[i] = readOne();
    }
    if ( lcd >= 1 && lcd <= 6 ) {
      print( lcds[lcd-1], line1, line2 );
    }
  }
}

void print( SoftwareSerial lcd, String line1, String line2 ) {
  lcd.print("sc;");
  delay(10);
  lcd.print("sd0,0;");
  delay(10);
  lcd.print("ss");
  lcd.print(line1);
  lcd.print(";");
  delay(10);
  lcd.print("sd1,0;");
  delay(10);
  lcd.print("ss");
  lcd.print(line2);
  lcd.print(";");
  delay(10);
}
