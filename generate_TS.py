import os
import wave
import random
import numpy as np


class GenerateTS:

    def __init__(self, f1, f2, fs=16000):
        self.f1 = f1
        self.f2 = f2
        self.fs = fs

    def generate_ts_tone(self):
        random.seed(os.urandom(4))
        theta = random.uniform(0, 2*np.pi)
        A = random.randint(0, 15000)
        std = random.uniform(0, 20000)
        T = 0.032
        numsamps = int(T * self.fs)
        t = np.arange(numsamps) * 1 / self.fs

        noise = np.random.normal(0, std, numsamps)

        tone = A * np.cos(2 * np.pi * self.f1 * t + theta) + A * np.cos(2 * np.pi * self.f2 * t + theta) + noise
        quantized_tone = tone.astype(np.int16)
        self.tone = quantized_tone

    def save_tone(self, filename):
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.fs)
            f.setnframes(len(self.tone))
            f.writeframesraw(self.tone)
            f.close()

DTMF_FREQS = {
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

def main():
    for key, freqs in DTMF_FREQS.items():
        f1, f2 = freqs
        if key in ['*', '#']:
            key = f'pound' if key == '#' else f'star'
        for i in range(100):
            gen = GenerateTS(f1, f2)
            gen.generate_ts_tone()
            gen.save_tone(f'./TS/{key}_{i+1:03d}.wav')
            print(f'{key} {i+1} done')
        
        # Generate test sets
        for i in range(10):
            gen = GenerateTS(f1, f2)
            gen.generate_ts_tone()
            gen.save_tone(f'./TEST/{key}_{i+1:03d}.wav')
            print(f'{key} {i+1} test done')

if __name__ == '__main__':
    main()  