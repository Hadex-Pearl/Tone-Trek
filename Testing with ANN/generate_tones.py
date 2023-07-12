import os
import sys
import math
import wave
import glob
import random
import numpy as np
import matplotlib.pyplot as plt

class SignalGenerator:
    def __init__(self):
        self.Fs = 16000.0
        self.N = 512
        self.f = np.asarray([697, 770, 852, 941, 1209, 1336, 1477, 1633], np.float64)
        self.t = np.arange(self.N)/self.Fs
        random.seed(os.urandom(4))
        self.distortions = []
        self.freqs = {
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
        self.load_distortions()

    def load_distortions(self):
        song_files = glob.glob('wav_audio_song/*.wav')
        talk_files = glob.glob('wav_audio_talk/*.wav')

        for file in song_files:
            with wave.open(file, 'r') as f:
                frames = f.readframes(-1)
                signal = np.frombuffer(frames, dtype='int16')
                self.distortions.append(signal)
                f.close()

        for file in talk_files:
            with wave.open(file, 'r') as f:
                frames = f.readframes(-1)
                signal = np.frombuffer(frames, dtype='int16')
                self.distortions.append(signal)
                f.close()

    def generate_training_data(self):
        for key, freq in self.freqs.items():
            f1, f2 = freq
            if key in ['*', '#']:
                key = 'pound' if key == '#' else 'star'
            for i in range(100):
                A = random.randint(0, 10000)
                phase = random.uniform(0, 2*np.pi)
                noise_signal = 3.0 * np.asarray([random.gauss(0, 1) for i in range(self.N)])

                song_talk = random.choice(self.distortions)
                song_talk = song_talk[:self.N].astype(np.float64)
                # normalize
                song_talk = 3.0 * song_talk / np.max(np.abs(song_talk))

                tone = np.cos(2*np.pi*f1*self.t + phase) + \
                    np.cos(2*np.pi*f2*self.t + phase) + \
                    noise_signal # + song_talk

                max_val = np.max(np.abs(tone))
                tone = tone/max_val * 32000
                int_tone = tone.astype(np.int16)

                with wave.open(f'./TS/{key}_{i+1:03d}.wav', 'w') as f:
                    f.setnchannels(1)
                    f.setsampwidth(2)
                    f.setframerate(self.Fs)
                    f.setnframes(len(int_tone))
                    f.writeframesraw(int_tone)
                    f.close()
                    print(f'{key} {i+1} done')

    def generate_test_data(self):
        for key, freq in self.freqs.items():
            f1, f2 = freq
            if key in ['*', '#']:
                key = 'pound' if key == '#' else 'star'
            for i in range(10):
                A = random.randint(0, 10000)
                phase = random.uniform(0, 2*np.pi)
                noise_signal = 3.0 * np.asarray([random.gauss(0, 1) for i in range(self.N)])

                song_talk = random.choice(self.distortions)
                song_talk = song_talk[:self.N].astype(np.float64)
                # Normalize
                song_talk = 3.0 * song_talk/np.max(np.abs(song_talk))

                tone = np.cos(2*np.pi*f1*self.t + phase) + \
                    np.cos(2*np.pi*f2*self.t + phase) + \
                    noise_signal # + song_talk

                max_val = np.max(np.abs(tone))
                tone = 32000/max_val * tone
                int_tone = tone.astype(np.int16)

                with wave.open(f'./TEST/{key}_{i+1:03d}.wav', 'w') as f:
                    f.setnchannels(1)
                    f.setsampwidth(2)
                    f.setframerate(self.Fs)
                    f.setnframes(len(int_tone))
                    f.writeframesraw(int_tone)
                    f.close()
                    print(f'{key} {i+1} test done')


# Create an instance of the SignalGenerator class
signal_generator = SignalGenerator()

# Generate training and test data
signal_generator.generate_training_data()
signal_generator.generate_test_data()
