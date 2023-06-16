# Tone-Trek
ToneTrek is an DTMF (Dual-Tone Multi-Frequency) demodulation repository designed to accurately decode and interpret DTMF signals. DTMF is a signaling technique used in telecommunication systems, commonly found in touch-tone telephone keypads, interactive voice response systems, and various other applications. 

## Initial commit
This has 2 python files, plots and dtmf tones with noise and without noise.

dtmf_generate.py generates the 16 tones of the dtmf and saves it in Tones (without noise) and Tones_n (with noise) directories.

dtmf_decode.py uses power spectral to decode the dtmf tone and plots the spectral for each tone in Plots (without noise) and Plots_n (with noise) directories.


## Generate Training Set
generate_TS.py: generates 100 training tones for each of the dtmf code and 10 test tones for each of the keys. To run this file, create a folder TS and TEST in the same directory as the code file to get the training and test data.

stacked_TS.py: stacks the 100 training set for each key into a single .dat file. This is done for all the other keys as well as the testing sets. To run this code, make sure the code file is in the same directory as the TS and TEST folders. Create a folder "stacked_sets" in the same directory as the code file.


## Training the model
train_model.py: trains a simple neural network using the training data. To run this code, make sure the code file is in the same directory as the stacked_sets folder.