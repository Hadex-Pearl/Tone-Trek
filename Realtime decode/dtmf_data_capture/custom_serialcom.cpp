/*
Simple serialcom routines
*/
#include <Arduino.h>
#include "custom_serialcom.h"

// Versions start at 10 
// "Commands" are sent from Arduino to RPi
// "Responses" are sent from RPi to Arduino
// Commands are 1 to 127
// Responses are 128 to 255
// Keys are magic numbers...just reducing probability of random error
#define CSC_KEY1 0xa5
#define CSC_KEY2 0x5a
#define CSC_PROT_VERSION 10
#define CSC_RESP_CONT 128

byte cmdbuf[4];
int data_cnt;

int csc_wait_on_pi(){
  int i;

  while(1){
    if(Serial.available() < 4){
      delay(10);
      continue;
    }
    Serial.readBytes(cmdbuf, 4);
    if( cmdbuf[0] == CSC_PROT_VERSION && 
        cmdbuf[1] == CSC_RESP_CONT &&
        cmdbuf[2] == CSC_KEY1 &&
        cmdbuf[3] == CSC_KEY2){
      return(0);
    }
  }
}

int csc_read_data(byte* databuf){
  int bytes2read;

  csc_wait_on_pi();

  cmdbuf[0] = CSC_PROT_VERSION;
  cmdbuf[1] = CSC_CMD_READ_PI;
  cmdbuf[2] = CSC_KEY1;
  cmdbuf[3] = CSC_KEY2;

  /* Send command and then Loop until the RPi responds */
  Serial.write(cmdbuf, 4);
  while(1){  
    if(Serial.available() < 2) continue;
    else break;
  }

  // Read the number of bytes to receive
  Serial.readBytes(cmdbuf, 2);
  bytes2read = (int)cmdbuf[0] + 
               (((int)cmdbuf[1]) << 8);

  // Read the data
  for(data_cnt = 0; data_cnt < bytes2read; data_cnt++){
    Serial.readBytes(&databuf[data_cnt], 1);
  }

  return(data_cnt);
}

int csc_write_data(int data_type, byte* databuf, int num_bytes){
  csc_wait_on_pi();

  // Send command
  cmdbuf[0] = CSC_PROT_VERSION;
  cmdbuf[1] = (byte)data_type;
  cmdbuf[2] = CSC_KEY1;
  cmdbuf[3] = CSC_KEY2;
  Serial.write(cmdbuf, 4);

  // Send data size to write
  cmdbuf[0] = num_bytes & 0xff;
  cmdbuf[1] = (num_bytes >> 8) & 0xff;
  Serial.write(cmdbuf, 2);

  // Write the data
  for(data_cnt = 0; data_cnt < num_bytes; data_cnt++){
    Serial.write(&databuf[data_cnt], 1);
  }  

  return(0);
}
