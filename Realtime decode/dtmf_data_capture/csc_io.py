#!/usr/bin/python3
import serial
import time

SIGNAL_ARD_READY = b'\x0a\x80\xa5\x5a'
CMD_READ_PI         = 2
CMD_WRITE_PI_ERROR  = 3
CMD_WRITE_PI_LOG    = 4
CMD_WRITE_PI_STATUS = 5
CMD_WRITE_PI_AUDIO  = 6

def rpi_init( devpath, baud_rate):
  global rpi_ser
  rpi_ser = serial.Serial(devpath, baudrate=baud_rate)

def rpi_send_string(rpi_str):
  databuf = f"{rpi_str}".encode('utf-8')
  i_datalen = len(databuf)
  b_datalen = i_datalen.to_bytes(2, 'little')
  rpi_ser.write(b_datalen)
  for i in range(i_datalen):
    rpi_ser.write(databuf[i:i+1])
    time.sleep(.00001)

def rpi_send_bytes(rpi_bytes):
  i_datalen = len(rpi_bytes)
  b_datalen = i_datalen.to_bytes(2, 'little')
  rpi_ser.write(b_datalen)
  for i in range(i_datalen):
    rpi_ser.write(rpi_bytes[i:i+1])
    time.sleep(.00001)

def rpi_get_ard_cmd():
    ard_cmd_total = rpi_ser.read(4)
	#print(f"command from Arduiono = {arc_cmd_total}")
    return( ard_cmd_total[1] )

def rpi_get_data():
  readval = rpi_ser.read(2)
  bytes2rcv = int.from_bytes(readval, 'little')
  readval = rpi_ser.read(bytes2rcv)
  return( readval )
  
def rpi_tell_ard_ready():
  rpi_ser.write( SIGNAL_ARD_READY )
