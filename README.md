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

