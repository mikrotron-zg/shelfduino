# shelfduino

Shelfduino is software for our electronic shelf.

It consists of two parts:
1) Arduino sketch
2) PC code, written in python

Both are designed written to be minimal.
Arduino part is smaller than 7kB, and can fit into smallest atmega MCU.
It requires only SoftwareSerial library, included in arduino IDE.
PC software is a web application to change individual screen content.
It requires only two python libraries: PyUSB and CherryPy.
These two communicate over USB by a simplistic protocol.

To start the software, run epolica.py found in src/pyton directory.

Hardware consists of:
1xArduino (any will do, or at least that's the idea)
6xSerial serial character screens (we used 16x2 serial modules by ITead)
6x 4 pin or 3 pin cables (depends on screens you use)
1xUSB cable (one you use with arduino)

Not required, but strongly recommended, is Arduino Sensor Shield.
You may use proto shield instead, but be prepared for hours of soldering.

Depending on power consumption of display modules used, additional power supply may be required (USB declares up to 500 mA).

Kit including all the required parts may be obtained from http://www.diykits.eu/
