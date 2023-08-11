#!/usr/bin/python3
import time
import sys
import csc_io as csc
import os.path
import os

if len( sys.argv ) != 1 :
  print("usage is: rpicom")
  sys.exit(1)

csc.rpi_init('/dev/ttyACM0', 115200)

filenum = 0
fdw = -1

start_time = time.time()
while(True):
  # Tell the Arduino we are ready to process a command
  csc.rpi_tell_ard_ready()

  # Read the command and process it
  ard_cmd = csc.rpi_get_ard_cmd()
  if ard_cmd == csc.CMD_READ_PI:
    # Arduino wants to read from RPi
    # print("Enter '1' to capture, '2' to stop")
    readval = 1  # Reads the terminal
    end_time = time.time()
    if( int( readval ) == 1 ):  
      if fdw != -1: 
        fdw.close()
        os.system(f"sox -r 16k -e signed -b 16 -c 1 -L {filein} {fileout}")
      filein =  f"dtmf_{filenum:03d}.raw"
      fileout = f"dtmf_{filenum:03d}.wav"
      fdw = open(filein, 'wb')
      filenum += 1
      if end_time - start_time >= 60:
        sys.exit(1)
    else:
      if fdw == -1 : print("WARNING: nothing was captured")
      fdw.close()
      os.system(f"sox -r 16k -e signed -b 16 -c 1 -L {filein} {fileout}")
      sys.exit(1)
    csc.rpi_send_string("3.1416") #sends the string
  elif ard_cmd == csc.CMD_WRITE_PI_ERROR:
    # Arduino is sending RPi an error message
    print(f"*** ERROR ***: {csc.rpi_get_data()}")
  elif ard_cmd == csc.CMD_WRITE_PI_LOG:
    # Arduino is sending RPi a log message
    print(f"LOG: {csc.rpi_get_data()}")
  elif ard_cmd == csc.CMD_WRITE_PI_STATUS:
    # Arduino is sending RPi a log message
    print(f"STATUS: {csc.rpi_get_data()}")
  elif ard_cmd == csc.CMD_WRITE_PI_AUDIO:
    audio_data = csc.rpi_get_data()
    # print(f"AUDIO: \n{audio_data.hex()}")
    fdw.write(audio_data)
    print(f"audio chunk received")
  else:
    print("ERROR: this shouldn't happen")
    sys.exit(1)
