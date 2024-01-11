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
        self.Fs = 8000 #16000.0
        self.N = 800 #512
        self.f = np.asarray([697, 770, 852, 941, 1209, 1336, 1477, 1633], np.float64)
        self.t = np.arange(self.N)/self.Fs
        random.seed(os.urandom(4)) # seed with 4 bytes of randomness from OS
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
        """
        Load distortions (song or talk) from wav files.

        Parameters:
        None

        Returns:
        None

        """
        song_files = glob.glob('wav_audio_song/*.wav')
        talk_files = glob.glob('wav_audio_talk/*.wav')

        count = 0
        for file in song_files:
            with wave.open(file, 'r') as f:
                frames = f.readframes(-1)
                signal = np.frombuffer(frames, dtype='int16')
                self.distortions.append(signal)
                f.close()
            count += 1
            print("Song processed: ", count)

        count = 0
        for file in talk_files:
            with wave.open(file, 'r') as f:
                frames = f.readframes(-1)
                signal = np.frombuffer(frames, dtype='int16')
                self.distortions.append(signal)
                f.close()
            count += 1
            print("Talk processed: ", count)

    def generate_data(self, data_size, noise=True, distortion=True, test=False):
        """ 
        Generates dataset.

        Parameters:
        data_size (int): number of samples to generate for each key
        noise (bool): whether to add noise to the signal
        distortion (bool): whether to add song or talk to the signal
        test (bool): whether to generate test data or training data

        Returns:
        None
        """
        for key, freq in self.freqs.items():
            f1, f2 = freq
            if key in ['*', '#']:
                key = 'pound' if key == '#' else 'star' 
            for i in range(data_size):
                A = random.randint(0, 10000)
                phase = random.uniform(0, 2*np.pi)

                tone = np.cos(2*np.pi*f1*self.t + phase) + \
                    np.cos(2*np.pi*f2*self.t + phase)

                if noise:
                    noise_signal = 3.0 * np.asarray([random.gauss(0, 1) for i in range(self.N)])
                    tone += noise_signal

                if distortion:
                    song_talk = random.choice(self.distortions)
                    song_talk = song_talk[:self.N].astype(np.float64)
                    # normalize
                    song_talk = 3.0 * song_talk / np.max(np.abs(song_talk))
                    tone += song_talk

                max_val = np.max(np.abs(tone))
                tone = tone/max_val * 32000
                int_tone = tone.astype(np.int16)

                # Save tones in a file
                filename = f'./{"TEST" if test else "TRAIN"}/{key}_{i+1:03d}.wav'
                with wave.open(filename, 'w') as f:
                    f.setnchannels(1)
                    f.setsampwidth(2)
                    f.setframerate(self.Fs)
                    f.setnframes(len(int_tone))
                    f.writeframesraw(int_tone)
                    f.close()
                    if test:
                        print(f'Key {key}, {i+1} test data saved')
                    else:
                        print(f'Key {key}, {i+1} training data saved')                    


# Create an instance of the SignalGenerator class
signal_generator = SignalGenerator()

# Generate training and test data
signal_generator.generate_data(data_size=1120)
signal_generator.generate_data(data_size=280, test=True)
