#!/usr/bin/env python

import usb
import serial
import types
import os
import sys, traceback
import io
import platform, glob
import time

#port = None
#sio = None
port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) 
sio = io.TextIOWrapper(io.BufferedRWPair(port, port))
spaces='                '

def scan():
  ids = { "04ca:3006":"ITeaduino Lite", "10c4:ea60":"ITeaduino Lite" }
  busses = usb.busses()
  shelfcnt = 0
  lcdcnt = 0 # lcd count
  lcds = {}

  # scan USB bus looking for devices with given ids
  for bus in busses:
    devices = bus.devices
    for dev in devices:
      nesto = "%04x" % dev.idVendor
      nesto = nesto + ":%04x" % dev.idProduct
      #print nesto
      if nesto in ids:
        #for config in dev.configurations:
        config = dev.configurations[0]
        #for intf in config.interfaces:
        iface = config.interfaces[0][0]
        shelfcnt = shelfcnt + 1

        print "e-Polica ", lcdcnt, "Device", dev.filename, nesto, ":", ids[nesto], "V"+dev.deviceVersion, "Max packet size:",dev.maxPacketSize
        #TODO: handshake, read properties, number of screens etc
        for portName in scanSerial():
          try:
            port = serial.Serial(portName, 9600, timeout=1) 
            sio = io.TextIOWrapper(io.BufferedRWPair(port, port))
            print "Found port:", portName
            time.sleep(3)
            sio.write(unicode('00'))
            sio.flush()
            if ( sio.read() == "OK" ):
              print "e-Polica - ", portName
          except serial.SerialException:
            pass
          
        lcdcnt = 6
        for i in range(1,lcdcnt+1):
          lcds['lcd%s'%i] = LCD(i)
        
  print lcds
  return lcds

def scanSerial():
  # scan for available ports. return a list of tuples (num, name)
  system_name = platform.system()
  if system_name == "Windows":
    # Scan for available ports.
    available = []
    for i in range(256):
      try:
        s = serial.Serial(i)
        available.append(i)
        s.close()
      except serial.SerialException:
        pass
    return available
  elif system_name == "Darwin":
    # Mac
    return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
  else:
    # Assume Linux or something else
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')        
  
class LCD:
  num = 0
  rows = 2
  cols = 16
  curText = ["",""]
  
  def __init__(self, num):
    self.num = num
    
  def fclose():
    self.fhandle.close()

  def write( self, args ):
    start='0%s'%self.num
    line1=args[0]+spaces[:len(spaces)-len(args[0])]
    line2=args[1]+spaces[:len(spaces)-len(args[1])]
    msg=start+line1+line2
    print msg
    
    sio.write(msg)
    sio.flush()
    
    self.curText = args
    time.sleep(.1)