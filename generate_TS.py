import os
import wave
import glob
import random
import numpy as np


class GenerateTS:

    def __init__(self, f1, f2, fs=16000):
        self.f1 = f1
        self.f2 = f2
        self.fs = fs

    def generate_ts_tone(self, song_talk, distortion=False):
        random.seed(os.urandom(4))
        theta = random.uniform(0, 2*np.pi)
        A = random.randint(0, 15000)
        std = random.uniform(0, 20000)
        T = 0.032
        numsamps = int(T * self.fs)
        t = np.arange(numsamps) * 1 / self.fs

        noise = np.random.normal(0, std, numsamps)
        if distortion:
            tone = A * np.cos(2 * np.pi * self.f1 * t + theta) + A * np.cos(2 * np.pi * self.f2 * t + theta) + noise + song_talk
        else:
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

    # Read songs and talks and add to a list
    distortion = []
    song_files = glob.glob('wav_audio_song/*.wav')
    talk_files = glob.glob('wav_audio_talk/*.wav')

    for song in song_files:
        with wave.open(song, 'r') as f:
            frames = f.readframes(-1)
            distortion.append(np.frombuffer(frames, dtype=np.int16))
            f.close()
    for talk in talk_files:
        with wave.open(talk, 'r') as f:
            frames = f.readframes(-1)
            distortion.append(np.frombuffer(frames, dtype=np.int16))
            f.close()
    # print("Number of songs and talks: ", len(distortion))


    for key, freqs in DTMF_FREQS.items():
        f1, f2 = freqs
        if key in ['*', '#']:
            key = f'pound' if key == '#' else f'star'
        for i in range(100):
            # Randomly select a song or talk and slice to fit the tone
            song_talk = random.choice(distortion)  
            start_index = random.randint(0, len(song_talk) - 512)
            stop_index = start_index + 512

            song_talk = song_talk[start_index:stop_index]    
            # print("Length of song or talk: ", len(song_talk))
            # print("Data type of song or talk: ", song_talk.dtype)

            gen = GenerateTS(f1, f2)
            gen.generate_ts_tone(song_talk, distortion=True)
            gen.save_tone(f'TS/{key}_{i+1:03d}.wav')
            print(f'{key} {i+1} done')
        
        # Generate test sets
        for i in range(10):
            # Randomly select a song or talk and slice to fit the tone
            song_talk = random.choice(distortion)  
            start_index = random.randint(0, len(song_talk) - 512)
            stop_index = start_index + 512

            song_talk = song_talk[start_index:stop_index]    
            # print("Length of song or talk: ", len(song_talk))
            # print("Data type of song or talk: ", song_talk.dtype)

            gen = GenerateTS(f1, f2)
            gen.generate_ts_tone(song_talk, distortion=True)
            gen.save_tone(f'TEST/{key}_{i+1:03d}.wav')
            print(f'{key} {i+1} test done')

if __name__ == '__main__':
    main()  