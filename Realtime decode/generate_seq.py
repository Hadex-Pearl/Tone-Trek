import os
import wave
import struct
import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(os.urandom(4))

# Constants for DTMF tones
freqs = {
    '1': (1209, 697),
    '2': (1336, 697),
    '3': (1477, 697),
    'A': (1633, 697),
    '4': (1209, 770),
    '5': (1336, 770),
    '6': (1477, 770),
    'B': (1633, 770),
    '7': (1209, 852),
    '8': (1336, 852),
    '9': (1477, 852),
    'C': (1633, 852),
    '0': (1336, 941),
    '*': (1209, 941),
    '#': (1477, 941),
    'D': (1633, 941)
}

samp_rate = 16000

# Generate one second of silence
silence = [0] * samp_rate
# print(len(silence))

# Generate a synchronization tone
num_samples = 512
freq = 1000
t = np.arange(num_samples) / samp_rate
sync_tone = np.cos(2 * np.pi * freq * t)
# print(len(sync_tone))

# Generate the DTMF sequence
dtmf_sequence = []

# Add one second of silence
dtmf_sequence.extend(silence)

# Add 2*512 samples of synchronization tone
dtmf_sequence.extend(sync_tone)
dtmf_sequence.extend(sync_tone)
# print(len(dtmf_sequence))

# Add 1024 samples of silence
dtmf_sequence.extend(silence[:1024])

# Add each DTMF tone to the sequence six times (3072 samples)
for key, freqs in freqs.items():
    f1, f2 = freqs
    phase = random.uniform(0, 2*np.pi)
    dtmf_tone = np.cos(2 * np.pi * f1 * t + phase) + np.cos(2 * np.pi * f2 * t + phase)
    dtmf_sequence.extend(dtmf_tone)
    dtmf_sequence.extend(dtmf_tone)
    dtmf_sequence.extend(dtmf_tone)
    dtmf_sequence.extend(dtmf_tone)
    dtmf_sequence.extend(dtmf_tone)
    dtmf_sequence.extend(dtmf_tone)
 
# print(len(dtmf_sequence))

# Repeat the sequence till we have 60 seconds of audio (960,000 samples)
while len(dtmf_sequence) < 960000:
    dtmf_sequence.extend(dtmf_sequence)

# print(len(dtmf_sequence))

# Trim the sequence to 60 seconds
dtmf_sequence = dtmf_sequence[:960000]
# print(len(dtmf_sequence))

# # print max and min value
# print(max(dtmf_sequence))
# print(min(dtmf_sequence))

# # Plot the DTMF sequence
# plt.plot(dtmf_sequence)
# plt.title('DTMF Sequence')
# plt.xlabel('Sample')
# plt.ylabel('Amplitude')
# plt.savefig('./dtmf_sequence.png')
# plt.close()


# Create a wave file
wave_filename = './dtmf_sequence.wav'
with wave.open(wave_filename, 'w') as f:
    f.setnchannels(1)  # Mono audio
    f.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
    f.setframerate(samp_rate)
    print(len(dtmf_sequence))
    f.setnframes(len(dtmf_sequence))

    # Normalize and convert the samples to binary format
    max_value = max(max(dtmf_sequence), abs(min(dtmf_sequence)))
    normalized_samples = [x / max_value for x in dtmf_sequence]
    scaled_samples = [int(x * 32767) for x in normalized_samples]
    packed_data = struct.pack('<' + 'h' * len(scaled_samples), *scaled_samples)
    f.writeframes(packed_data)
    f.close()

# print(f"DTMF sequence saved as '{wave_filename}'.")


# # Rough code to detect the sync tone
# tone = dtmf_sequence[16000:16512]
# print(max(tone))

# # Calculate pure sine and cosine waves
# N = 512
# t = np.arange(N) / 16000
# # print(t)

# freqs = [697, 770, 852, 941, 1000, 1209, 1336, 1477, 1633]
# sin_tones = np.zeros((9, N), dtype=np.float64)
# cos_tones = np.zeros((9, N), dtype=np.float64)
# fs = 16000
# for i, freq in enumerate(freqs):
#     cos_tones[i] = np.cos(2 * np.pi * freq * t)
#     sin_tones[i] = np.sin(2 * np.pi * freq * t)
# # print(sin_tones)
# # Compute dot product of tones
# sin_prod = np.dot(tone, sin_tones.T)
# cos_prod = np.dot(tone, cos_tones.T)
# # print(sin_prod)
# # print(cos_prod)

# # Compute power of tones
# pow_tones = cos_prod**2 + sin_prod**2
# # print(pow_tones)

# # Normalize power
# max_val = np.max(pow_tones)
# print(max_val)
# # pow_tones = pow_tones / max_val
# # print(pow_tones)

# # Convert power to dB
# pow_tones = 10 * np.log10(pow_tones)
# print(pow_tones)

# # plot power
# plt.plot(freqs, pow_tones)
# plt.title('Power of tones')
# plt.xlabel('Tone')
# plt.ylabel('Power (dB)')
# plt.show()

