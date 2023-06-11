import numpy as np
import wave
import matplotlib.pyplot as plt

def compute_purewave(freqs, N, cosine=True):
    d = len(freqs)
    A = np.zeros((d, N))
    fs = 16000
    n = np.arange(N)/fs
    for i, f in enumerate(freqs):
        if cosine:
            A[i] = 10000 * np.cos(2 * np.pi * f * n)
        else:
            A[i] = 10000 * np.sin(2 * np.pi * f * n)
        A[i] = A[i].astype(np.int16)
    return A

def read_wave(filename):
    with wave.open(filename, 'r') as f:
        frames = f.readframes(-1)
        tone = np.frombuffer(frames, dtype=np.int16)
        return tone

DTMF_rows = np.array([697, 770, 852, 941])
DTMF_cols = np.array([1209, 1336, 1477, 1633])

DTMF_FREQS = np.concatenate((DTMF_rows, DTMF_cols))
symbols = ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']
N = 512

cos_ideal = compute_purewave(DTMF_FREQS, N, cosine=True)
sin_ideal = compute_purewave(DTMF_FREQS, N, cosine=False)
# print(cos_ideal[0])

# Read audio from wave files
tones = np.zeros((len(symbols), N)) # Without noise
tones_n = np.zeros((len(symbols), N)) # With noise
for i, symbol in enumerate(symbols):
    if symbol in ['*', '#']:
        symbol = 'pound' if symbol == '#' else 'star'
    filename = 'Tones/dtmf_' + symbol + '.wav' # Without noise
    filename_n = 'Tones_n/dtmf_' + symbol + '_noise.wav' # With noise
    tones[i] = read_wave(filename) # Without noise
    tones_n[i] = read_wave(filename_n) # With noise

# Dot multiply the ideal waveforms with the actual waveforms to get the dot product (without noise)
cos_dot = np.matmul(tones, cos_ideal.T)
sin_dot = np.matmul(tones, sin_ideal.T)
power = cos_dot**2 + sin_dot**2

# Dot multiply the ideal waveforms with the actual waveforms to get the dot product (with noise)
cos_dot_n = np.matmul(tones_n, cos_ideal.T)
sin_dot_n = np.matmul(tones_n, sin_ideal.T)
power_n = cos_dot_n**2 + sin_dot_n**2

# Convert each value in DTMF_FREQS to a string
FREQS = DTMF_FREQS.astype(str)

# Plot bar chart of power without noise
for i, symbol in enumerate(symbols):
    plt.plot(FREQS, power[i], 'ro')
    plt.bar(FREQS, power[i], width=0.03, color='b')
    plt.grid(True)
    plt.title('Power of key ' + symbol + ' (without noise)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    if symbol in ['*', '#']:
        symbol = 'pound' if symbol == '#' else 'star'
    plt.savefig('Plots/' + symbol + '.png')
    plt.close()

# Plot bar chart of power with noise
for i, symbol in enumerate(symbols):
    plt.plot(FREQS, power_n[i], 'ro')
    plt.bar(FREQS, power_n[i], width=0.03, color='b')
    plt.grid(True)
    plt.title('Power of key ' + symbol + ' (with noise)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    if symbol in ['*', '#']:
        symbol = 'pound' if symbol == '#' else 'star'
    plt.savefig('Plots_n/' + symbol + '.png')
    plt.close()