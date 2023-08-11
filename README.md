# Tone-Trek
ToneTrek is an DTMF (Dual-Tone Multi-Frequency) demodulation repository designed to accurately decode and interpret DTMF signals. DTMF is a signaling technique used in telecommunication systems, commonly found in touch-tone telephone keypads, interactive voice response systems, and various other applications. 

## Initial commit
This has 2 python files, plots and dtmf tones with noise and without noise. Which is now included in the Preliminary test folder.

dtmf_generate.py generates the 16 tones of the dtmf and saves it in Tones (without noise) and Tones_n (with noise) directories. To run this file, create a folder Tones and Tones_n in the same directory as the code file to get the tones.

```python dtmf_generate.py```

dtmf_decode.py uses power spectral to decode the dtmf tone and plots the spectral for each tone in Plots (without noise) and Plots_n (with noise) directories. To run this file, create a folder Plots and Plots_n in the same directory as the code file to get the plots.

```python dtmf_decode.py```

Look at the spikes in the plot to identify the frequencies and hence the key detected.

# Testing with ANN
## Generate Training Set
generate_tones.py: generates 100 training tones for each of the dtmf code and 10 test tones for each of the keys. To run this file, create a folder TS and TEST in the same directory as the code file to get the training and test data.

stacked_TS.py: stacks the 100 training set for each key into a single .dat file. This is done for all the other keys as well as the testing sets. To run this code, make sure the code file is in the same directory as the TS and TEST folders. Create a folder "stacked_tones" in the same directory as the code file.

## Training the model
train_model.py: trains a simple neural network using the training data. To run this code, make sure the code file is in the same directory as the stacked_tones folder.

# Real Time DTMF Detection on Raspberry Pi/Arduino
## Generate sequence of tones
generate_seq.py: generates a sequence of dtmf tones preceeded by a synchronization tone of frequency 1000Hz. This frequency is used to synchronize the receiver and the transmitter. After generating the tone, it is played to the Arduino nanosense BLE with an audio sensor to capture the tones.

## Capture the tones on Arduino
The Arduino code is in the folder "dtmf_data_capture". The code is uploaded to the Arduino Nano 33 BLE sense. The code captures the tones and stores it in a buffer. The buffer is then sent to the Raspberry Pi via BLE.

This Arduino code performs audio processing using the PDM (Pulse Density Modulation) microphone to analyze incoming audio data. Here's a summary of what the code is doing:

1. Include Libraries: The code includes necessary libraries for Arduino, PDM microphone handling, and a custom serial communication module.

2. Define LED Pins: Pin numbers for different LED colors are defined using constants.

3. Global Variables: Various global variables are declared to store audio data, frequencies, sine and cosine wave values, power calculations, and timing information.

4. Setup Function:

    - Initializes the LED pins.
    - Initializes the PDM microphone with a gain of 200 and a sample rate of 16000 Hz.
    - Creates pure sine and cosine wave signals which would be used in detecting frequencies present in a captured tone.

5. onPDMdata Function:

    - Handles the callback for PDM data reception.
    - Reads audio data into the sample buffer based on the audio_capture flag.

6. Loop Function:

    - Waits for a signal from another device (RPi) using csc_read_data function.
    - sets up to capture audio data.
    - Continuously processes audio data until a target sample count is reached.
    - Communicates the processing status using HandleOutput_status.
    - Detects the frequency of the captured tone using power:
        - Calculates dot products between audio data and sine/cosine waveforms for different frequencies.
        - Calculate and normalizes the power values and detects a specific frequency range based on power levels.
        - Controls LEDs to indicate the detection result and communicates the detected frequency using HandleOutput_int.

7. Output Handling Functions:

    Several functions are defined to handle different types of data output to the RaspberryPi. These functions package and send data using a custom serial communication protocol.

8. Light LED Function:

    A function to control LED colors by turning specific pins on or off.

## Capture the tones on Raspberry Pi
The Raspberry Pi code is in the folder "dtmf_data_capture". The code is run on the Raspberry Pi 4. The code captures the tones and stores it in a buffer. The buffer is then sent to the Raspberry Pi via BLE.

This Raspberry Pi code performs audio processing using the PDM (Pulse Density Modulation) microphone to analyze incoming audio data. Here's a summary of what the code is doing:

1. Include Libraries: The code includes necessary libraries for Raspberry Pi. The code also includes a custom serial communication module.

2. Initializing Communication: The script initializes communication with the Arduino by calling csc.rpi_init() with the serial port and baud rate.

3. Loop Function:

    - The script enters an infinite loop.
    - It notifies the Arduino that the Raspberry Pi is ready to process a command by calling csc.rpi_tell_ard_ready().
    - It reads the command sent by the Arduino using csc.rpi_get_ard_cmd().
    - Depending on the received command, different actions are taken:

        - If the command is CMD_READ_PI (indicating the Arduino wants to read from the Raspberry Pi), the script:
            - Prompts the user to enter '1' to start capturing audio or '2' to stop.
            - If '1' is entered, it opens a binary file for writing audio data.
            - If '2' is entered, it closes the file and converts the captured raw audio data to WAV format using the "sox" utility.
        - If the command is CMD_WRITE_PI_ERROR, it prints the error message received from the Arduino.
        - If the command is CMD_WRITE_PI_LOG, it prints the log message received from the Arduino.
        - If the command is CMD_WRITE_PI_STATUS, it prints the status message received from the Arduino.
        - If the command is CMD_WRITE_PI_AUDIO, it receives audio data from the Arduino, writes it to the file descriptor (fdw), and prints an acknowledgment.
        - If the command is none of the above, it prints an error message and exits the script.

Note:

    1. The script uses a custom serial communication protocol (provided by the csc_io module) to interact with the Arduino.
    2. The script captures and processes audio data from the Arduino, converting it to WAV format using the "sox" utility.
    3. Depending on user input, it starts and stops audio data capture and processing.