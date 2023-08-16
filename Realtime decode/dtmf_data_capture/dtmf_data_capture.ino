#include <Arduino.h>
#include <PDM.h>                 // microphone
#include "avr/dtostrf.h"
#include "custom_serialcom.h"

// For use with the LED
#define RED_PIN 22
#define GREEN_PIN 23
#define BLUE_PIN 24
#define YELLOW_PIN LED_BUILTIN
#define NO_PIN -1

// Globals
namespace{
  char logbuf[128];

  // Default PDM buffer size is 256 samples (512 bytes)
  // At 16Khz, there are 62.5 buffers captured per second
  const int pdm_buf_size = 1024;
  const int num_buf_bytes = pdm_buf_size;
  const int num_buf_samples = pdm_buf_size / 2;
  const int num_bufs = 1;  
  const int samples = num_buf_samples * num_bufs;
  short audio_data[num_bufs * num_buf_samples] = {0}; // holds good audio
  short audio_junk[num_buf_samples]; // holds junk audio
  volatile int buf_ctr;
  volatile int proc_ctr;
  int old_buf_ctr;

  int samples_processed;
  int target_samples = num_bufs * num_buf_samples;
  int audio_capture = 0;

  const int freqs[9] = {697, 770, 852, 941, 1000, 1209, 1336, 1477, 1633};
  double sin_tones[9][samples];
  double cos_tones[9][samples];
  double t[samples];
  double sin_dot[9];
  double cos_dot[9];
  double power[9];

  unsigned long total_time;
}

void setup(){
  proc_ctr = 0;
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  light_led(NO_PIN);

	HandleOutput_status( -1 ); // setup() starting
  // HandleOutput_int( num_buf_bytes );
  // HandleOutput_int( num_buf_samples );
  // HandleOutput_int( num_bufs );
  PDM.onReceive(onPDMdata);
  PDM.setGain(200);  // default is 20
  if (!PDM.begin(1, 16000) ){
    HandleOutput_error( -1000 );
    while(1);
  }
  /*
  // Spin for 4 seconds.  This allows transients in the microphone
  // to dissipate (they appear to be caused by the PDM enable operations
  // above)
  unsigned int go_on = micros() + 4000000;
  while(micros() < go_on);
  */
	HandleOutput_status( -2 ); // setup() ending

  // Create pure sine and cosine waves for each frequency
   for (int i = 0; i < samples; i++) {
      t[i] = i / 16000.0;
      // cout <<t[i] << endl;
  }
  for (int i = 0; i < 9; i++) {
      for (int j = 0; j < samples; j++) {
          sin_tones[i][j] = sin(2 * M_PI * freqs[i] * t[j]);
          cos_tones[i][j] = cos(2 * M_PI * freqs[i] * t[j]);
      }
  }
}

void onPDMdata() {
  // Read audio data into the sample buffer.
  // Note that until audio_capture == 1, we just keep overwriting
  // the same junk location.  This is all to avoid ever turning
  // audio capture off once it is started.
  if( audio_capture == 1 ){
    PDM.read(&audio_data[buf_ctr*num_buf_samples], num_buf_bytes);
    buf_ctr++;
    if( buf_ctr == num_bufs ) audio_capture = 0;
  }
  else{
    PDM.read(&audio_junk[0], num_buf_bytes);
  } 
  proc_ctr++; 
}

void loop(){
  while(1){
    // This pauses us until the RPi is ready to do another capture.
    // The RPi signals it is ready to capture by sending
    // an arbitrary string value to the Arduino
    csc_read_data( (byte*) logbuf );
    HandleOutput_status( -3 );
    buf_ctr = old_buf_ctr = samples_processed = 0;
    audio_capture = 1;
    while(audio_capture == 1){
      // Sleep for 5ms
      delay(5);
      // if(old_buf_ctr != buf_ctr){
      //   old_buf_ctr = old_buf_ctr + 1;
      //   samples_processed += num_buf_samples;
      //   if( samples_processed >= target_samples ) break;
      // }
    }
    int temp_ctr = proc_ctr;
    HandleOutput_status(-4); // tell RPi where we're at
    // Send the audio to the RPi
    // HandleOutput_audio((byte*)audio_data, num_bufs*num_buf_bytes);
    
    // compute dot product of captured audio and purewaves
    for (int i = 0; i < 9; i++) {
        sin_dot[i] = 0;
        cos_dot[i] = 0;
    }
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < samples; j++) {
            sin_dot[i] += audio_data[j] * sin_tones[i][j];
            cos_dot[i] += audio_data[j] * cos_tones[i][j];
        }
        // Compute power
        power[i] = sin_dot[i] * sin_dot[i] + cos_dot[i] * cos_dot[i];
    }

    // normalize power
    double max_power = 0;
    for (int i = 0; i < 9; i++) {
        if (power[i] > max_power) {
            max_power = power[i];
        }
    }
    // Define a treshold for detection
    if (max_power < 100000000) {
      // Light red LED
      // light_led(RED_PIN);
      // delay(100);
      // light_led(NO_PIN);
      // Print "No freq detected"
      HandleOutput_int(-1);
    } else {
    for (int i = 0; i < 9; i++) {
        power[i] /= max_power;
    }

    // Convert power to dB
    double power_db[9];
    for (int i = 0; i < 9; i++) {
        power_db[i] = 10 * log10(power[i]);
    }

    // find index of power_db == 0
    int index = 0;
    for (int i = 0; i < 9; i++) {
        if (power_db[i] == 0) {
            index = i;
        }
    }
    
    // Light green LED if sync tone detected
    if (freqs[index] == 1000) {
      light_led(GREEN_PIN);
      delay(100);
      light_led(NO_PIN);
    } //else {
    //   light_led(BLUE_PIN);
    //   delay(100);
    //   light_led(NO_PIN);
    // }
    HandleOutput_int(freqs[index]);
    }
    HandleOutput_status(-5);
    // PDM.end();
    HandleOutput_int(proc_ctr - temp_ctr);
  }
}

/*
These functions send data to the RPi from the Arduino.
The data is tagged differently when sent to the RPi depending
on which of these functions is called
*/

void HandleOutput_int(int log_int){
	itoa(log_int, logbuf, 10);
	csc_write_data(CSC_CMD_WRITE_PI_LOG, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_short(short log_int){
	itoa(log_int, logbuf, 10);
	csc_write_data(CSC_CMD_WRITE_PI_LOG, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_uint(unsigned int log_int){
	utoa(log_int, logbuf, 10);
	csc_write_data(CSC_CMD_WRITE_PI_LOG, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_double(double log_double){
	dtostrf(log_double, 10, 3, logbuf);
	csc_write_data(CSC_CMD_WRITE_PI_LOG, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_double_ptr(double* log_double){
    dtostrf(*log_double, 10, 3, logbuf);
    csc_write_data(CSC_CMD_WRITE_PI_LOG, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_status(int status){
	itoa(status, logbuf, 10);
	csc_write_data(CSC_CMD_WRITE_PI_STATUS, (byte*)logbuf, strlen(logbuf) );
}
void HandleOutput_error(int error_code){
	itoa(error_code, logbuf, 10);
	csc_write_data(CSC_CMD_WRITE_PI_ERROR, (byte*)logbuf, strlen(logbuf) );
}

// Output audio
void HandleOutput_audio(byte* data_buf, int data_len){
  // max size we can output in one call is 65535
  int left_to_output = data_len;
  int chunk_ctr = 0;
  while( left_to_output >= 65535){ 
    csc_write_data(CSC_CMD_WRITE_PI_AUDIO, &data_buf[chunk_ctr*65535], 65535);
    left_to_output -= 65535;
    chunk_ctr++;
  }
  if( left_to_output > 0 ){
    csc_write_data(CSC_CMD_WRITE_PI_AUDIO, &data_buf[chunk_ctr*65535], 
                   left_to_output);
  }
}

void light_led(int color) {
  if (color == NO_PIN) {  // turn off all the LEDs
    // These pins are asserted low
    digitalWrite(RED_PIN, HIGH);
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(BLUE_PIN, HIGH);
    // This pin is asserted high
    // (FYI so is the power pin which we don't use)
    digitalWrite(YELLOW_PIN, LOW);
  } else {  // Turn on the pin you want
    if (color == YELLOW_PIN) {
      digitalWrite(color, HIGH);
    } else {
      digitalWrite(color, LOW);
    }
  }
}
