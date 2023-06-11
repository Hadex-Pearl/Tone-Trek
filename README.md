# Tone-Trek
ToneTrek is an DTMF (Dual-Tone Multi-Frequency) demodulation repository designed to accurately decode and interpret DTMF signals. DTMF is a signaling technique used in telecommunication systems, commonly found in touch-tone telephone keypads, interactive voice response systems, and various other applications. 

# Initial commit
This has 2 python files, plots and dtmf tones with noise and without noise.

dtmf_generate.py generates the 16 tones of the dtmf and saves it in Tones (without noise) and Tones_n (with noise) directories.

dtmf_decode.py uses power spectral to decode the dtmf tone and plots the spectral for each tone in Plots (without noise) and Plots_n (with noise) directories.
