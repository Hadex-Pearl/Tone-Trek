import numpy as np
import wave
import matplotlib.pyplot as plt

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

class GenerateDTMF:
    def __init__(self, f1, f2, fs=16000):
        self.f1 = f1
        self.f2 = f2
        self.fs = fs  # sampling rate

    def generate_dtmf_tone(self, noise=False):
        """
        Generate a DTMF tone with frequencies f1 and f2 for duration seconds at
        sampling rate fs.

        Parameters:
        f1 (float): frequency of first tone
        f2 (float): frequency of second tone
        fs (int): sampling rate in Hz
        """
        A = 10000
        T = 0.032
        numsamps = int(T * self.fs)
        t = np.arange(numsamps) * 1 / self.fs

        tone = A * np.cos(2 * np.pi * self.f1 * t) + A * np.cos(2 * np.pi * self.f2 * t)
        if noise:
            std_dev = np.random.uniform(0, 20000)
            noise = np.random.normal(0, std_dev, numsamps)
            tone += noise
        quantized_tone = tone.astype(np.int16)
        self.tone = quantized_tone

    def save_tone(self, filename):
      """
      Save a tone to a file.

      Parameters:
      filename (str): filename to save
      """
      with wave.open(filename, 'w') as f:
          f.setnchannels(1)
          f.setsampwidth(2)
          f.setframerate(16000)
          f.writeframes(self.tone.tobytes())
          f.close()

    def plot_tone(self):
        """
        Plot the tone.
        """
        plt.plot(self.tone)
        plt.show()


def main():
    # Generate all DTMF tones and save it to a file.
    for key, freqs in DTMF_FREQS.items():
        f1, f2 = freqs
        if key in ['*', '#']:
            key = f'pound' if key == '#' else f'star' # pound or star for filename
        gen = GenerateDTMF(f1, f2)
        # Without noise
        gen.generate_dtmf_tone()
        gen.save_tone(f'Tones/dtmf_{key}.wav')
        print(f'Saved tone {key}.')
        # With noise
        gen.generate_dtmf_tone(noise=True)
        gen.save_tone(f'Tones_n/dtmf_{key}_noise.wav')
        print(f'Saved tone {key} with noise.')

if __name__ == '__main__':
    main()
    