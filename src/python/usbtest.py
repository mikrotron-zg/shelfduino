#!/usr/bin/env python

import usb
import types
import os

UNIDIRECTIONAL_PROTOCOL  = 0x01
BIDIRECTIONAL_PROTOCOL  = 0x02
IEEE1284_4_PROTOCOL    = 0x03
VENDOR_PROTOCOL      = 0xff

class LCD:
  def __init__(self, device, configuration, interface):
    """
    __init__(device, configuration, interface) -> None

    Initialize the device.
      device: printer usb.Device object.
      configuration: printer usb.Configuration object of the Device or configuration number.
      interface: printer usb.Interface object representing the
                 interface and altenate setting.

    """

    self.__devhandle = device.open()
    #self.__devhandle.setConfiguration(configuration)
    #self.__devhandle.claimInterface(interface)
    #self.__devhandle.setAltInterface(interface)

    self.__intf = interface.interfaceNumber
    self.__alt  = interface.alternateSetting

    self.__conf = (type(configuration) == types.IntType \
            or type(configuration) == types.LongType) and \
            configuration or \
            configuration.value

    # initialize members
    # TODO: automatic endpoints detection
    self.__bulkout  = 1
    self.__bulkin  = 0x82

  def __del__(self):
    try:
      self.__devhandle.releaseInterface(self.__intf)
      del self.__devhandle
    except:
      pass

  def getDeviceID(self, maxlen, timeout = 100):
    """
    getDeviceID(maxlen, timeout = 100) -> device_id

    Get the device capabilities information.
      maxlen: maxlength of the buffer.
      timeout: operation timeout.
    """
    return self.__devhandle.controlMsg(requestType = 0xa1,
                       request = 0,
                       value = self.__conf - 1,
                       index = self.__alt + (self.__intf << 8),
                       buffer = maxlen,
                       timeout = timeout)

  def getPortStatus(self, timeout = 100):
    """
    getPortStatus(timeout = 100) -> status

    Get the port status.
      timeout: operation timeout.
    """
    return self.__devhandle.controlMsg(requestType = 0xa1,
                       request = 1,
                       value = 0,
                       index = self.__intf,
                       buffer = 1,
                       timeout = timeout)[0]

  def softReset(self, timeout = 100):
    """
    softReset(timeout = 100) -> None

    Request flushes all buffers and resets the Bulk OUT
    and Bulk IN pipes to their default states.
      timeout: the operation timeout.
    """
    self.__devhandle.controlMsg(requestType = 0x21,
                    request = 2,
                    value = 0,
                    index = self.__intf,
                    buffer = 0)


  def write(self, buffer, timeout = 100):
    """
    write(buffer, timeout = 100) -> written

    Write data to screen.
      buffer: data buffer.
      timeout: operation timeout.
    """
    return self.__devhandle.bulkWrite(self.__bulkout,
                      buffer,
                      timeout)

  def read(self, numbytes, timeout = 100):
    """
    read(numbytes, timeout = 100) -> data

    Read data - N/A.
      numbytes: number of bytes to read.
      timeout: operation timeout.
    """
    return self.__devhandle.bulkRead(self.__bulkin,
                     numbytes,
                     timeout)


ids = { "0403:6001":"gravitech", "239a:0001":"adafruit", "04d8:fa97":"seeedstudio" }
busses = usb.busses()
cnt = 0
usbcnt = 0
acmcnt = 1
tty = "unknown"

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
      cnt = cnt + 1
      #print "    Interface:",iface.interfaceNumber
      aman = LCD(dev, config, iface)
      print "EKRAN ", cnt, "Device", dev.filename, nesto, ":", ids[nesto], "V"+dev.deviceVersion, "Max packet size:",dev.maxPacketSize
      #print"  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor), "  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct)
      #print "  Device class:",dev.deviceClass, "Device sub class:",dev.deviceSubClass
      #aman.write( "Ekran "+cnt );
      tty = "/dev/ttyNotAvailable"
      if "gravitech" == ids[nesto]:
        while not os.path.exists( tty ):
          tty = "/dev/ttyUSB%i"%usbcnt
          usbcnt += 1
      elif "adafruit" == ids[nesto] or "seeedstudio"  == ids[nesto]:
        while not os.path	.exists( tty ):
          tty = "/dev/ttyACM%i"%acmcnt
          acmcnt += 1
      elif "test" == ids[nesto]:
        tty = "/dev/tty%i"%acmcnt
        acmcnt += 1
      print tty
      f = open(tty,'w');
      msg = "Ekran %i"%cnt+' '+tty
      f.write( msg )
