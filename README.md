# DTMF-Lab
This lab is an experiment, designed to accurately decode and interpret DTMF signals. DTMF is a signaling technique used in telecommunication systems, commonly found in touch-tone telephone keypads, interactive voice response systems, and various other applications. The experiment is divided into three parts: the first part is to decode DTMF signals using a simple power spectral analysis, the second part is to decode DTMF signals using a neural network and the third part uses real-time decoding of the DTMF signal using Arduino nano 33 BLE sense.

## Part 1: Preliminary Test
This has 2 python files.

1. dtmf_generate.py generates the 16 tones of the dtmf and saves it in Tones (without noise) and Tones_n (with noise) directories. 
    - To run this file, create a folder "Tones" and "Tones_n" in the same directory as the code file to get the tones.

2. dtmf_decode.py uses power spectral to decode the dtmf tone and plots the spectral for each tone in Plots (without noise) and Plots_n (with noise) directories. 
    - To run this file, create a folder "Plots" and "Plots_n" in the same directory as the code file to get the plots.

Look at the spikes in the plots to identify the frequencies and hence the key detected.

## Part 2: Testing with ANN
This folder has 3 python files.

### Generate Training Set
1. generate_tones.py: generates 1120 training tones for each of the dtmf keys and 280 test tones for each of the keys. 
    - To run this file, create a folder "TRAIN" and "TEST" in the same directory as the code file to get the training and test data.
    - When generating dataset, take note of the boolean variables, noise and distortion to determine it's presence in the dataset you want to generate.

2. stacked_TS.py: stacks the 1120 training set and 280 test set for each key into a single ".dat" file for easy use on tensorflow. 
    - To run this code, make sure the code file is in the same directory as the "TRAIN" and "TEST" folders.
    - Create a folder "stacked_tones" in the same directory as the code file.

### Training the model
3. train_model.py: trains a simple neural network using the training data. Converts the model to a tensorflow lite model (with and withot quantization) and saves it in the same directory as the code file. 
    - To run this code, make sure the code file is in the same directory as the stacked_tones folder.

## Part 3: Real Time DTMF Detection on Raspberry Pi/Arduino
This part is contained in the Realtime decode folder. this experiment also takes place in 3 parts.
    1. Collecting dataset using Arduino
    2. Training a model on PC using TensorflowLite
    3. Deploying model to Arduino and detecting DTMF tone realtime.

### Collecting dataset using Arduino
This would require a synchronization between the transmiter(Any device with microphone used in playing the tone. E.g PC or phone) and the receiver(Arduino). This is done by playing a 1000Hz synchronization tone before playing the DTMF tone. The Arduino would then use the 1000Hz tone to synchronize with the transmitter. The Arduino would then capture the DTMF tone and store it in a buffer. The buffer is then sent to RaspberryPi which saves the buffer to a file.

#### Generate sequence of tones
1. generate_seq.py: generates a sequence of dtmf tones preceeded by a synchronization tone of frequency 1000Hz. This frequency is used to synchronize the receiver and the transmitter. After generating the tone, it is played to the Arduino nanosense BLE with an audio sensor to capture the tones.
    - After running this code, a one minute .wav file containing the sequence is generated in the same folder the code is being ran.

#### Capture the tones on Arduino
The Arduino code is in the folder "dtmf_data_capture". The code is uploaded to the Arduino Nano 33 BLE sense. The code captures the tones and stores it in a buffer. The buffer is then sent to the Raspberry Pi.

This Arduino code performs audio processing using the PDM (Pulse Density Modulation) microphone to analyze incoming audio data. Here's a summary of what the code is doing:

1. Setup Function:

    - Initializes the LED pins.
    - Initializes the PDM microphone with a gain of 200 and a sample rate of 16000 Hz.
    - Creates pure sine and cosine wave signals which would be used in detecting frequencies present in a captured tone.

2. onPDMdata Function:

    - Handles the callback for PDM data reception.
    - Reads audio data into the sample buffer based on the audio_capture flag.

3. Loop Function:

    - Waits for a signal from another device (RPi) using csc_read_data function.
    - sets up to capture audio data.
    - Continuously processes audio data until a target sample count is reached.
    - Communicates the processing status using HandleOutput_status.
    - Detects the frequency of the captured tone using power:
        - Calculates dot products between audio data and sine/cosine waveforms for different frequencies.
        - Calculate and normalizes the power values and detects a specific frequency range based on power levels.
        - Controls LEDs to indicate the detection result and communicates the detected frequency using HandleOutput_int.

To compile the code: ```arduino-cli compile --fqbn arduino:mbed:nano33ble dtmf_data_capture``` 
To upload the code: ```arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed:nano33ble dtmf_data_capture```

Note: Do this in the Realtime decode folder on your terminal.


#### Sending tones to Raspberry Pi
The Raspberry Pi code "rpicom.py" is in the folder "dtmf_data_capture". The code captures the tones and stores it in a buffer. Here is a summary of what it does:

1. Initializing Communication: The script initializes communication with the Arduino by calling csc.rpi_init() with the serial port and baud rate.

2. Loop Function:

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