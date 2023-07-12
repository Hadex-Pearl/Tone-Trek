import sys
import os
import wave
import random
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

tf.keras.utils.set_random_seed(124)
np.random.seed(75)

filedir = "../stacked_tones/"
characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "pound", "star"]

# Create a dictionary of training and test files
TS = {character: filedir + "ts_" + character + ".dat" for character in characters}
TEST = {character: filedir + "test_" + character + ".dat" for character in characters}

# Read tones and create labels
X_train = np.empty((0, 512), dtype=np.int16)
y_train = np.empty((0, 1), dtype=int)
X_test = np.empty((0, 512), dtype=np.int16)
y_test = np.empty((0, 1), dtype=int)
label = 0
for symbol in TS.keys():
    f = open(TS[symbol], "rb")
    while True:
        # Read training data
        atone = np.fromfile(f, np.int16, 512)
        if atone.size < 512:
            break
        X_train = np.vstack((X_train, atone))
    f.close()
    num_ts_tones = X_train.shape[0] - y_train.shape[0]
    y_train = np.vstack((y_train, np.full((num_ts_tones, 1), label)))
    g = open(TEST[symbol], "rb")
    
    while True:
        # Read test data
        atone = np.fromfile(g, np.int16, 512)
        if atone.size < 512:
            break
        X_test = np.vstack((X_test, atone))
    g.close()
    num_test_tones = X_test.shape[0] - y_test.shape[0]
    y_test = np.vstack((y_test, np.full((num_test_tones, 1), label)))
    label += 1

# print(X_train.shape)
# print(y_train.shape)
# print(X_test.shape)
# print(y_test.shape)
print(np.max(abs(X_train)))

# Preprocessing the data
# Generate pure tones
N = 512
freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
sin_tones = np.zeros((8, N), dtype=np.float64)
cos_tones = np.zeros((8, N), dtype=np.float64)
fs = 16000
n = np.arange(N)/fs
for i, freq in enumerate(freqs):
    cos_tones[i] = (10000 * np.cos(2 * np.pi * freq * n))
    sin_tones[i] = (10000 * np.sin(2 * np.pi * freq * n))
# print(sin_tones.shape)
# print(sin_tones.dtype)
# print(sin_tones[0])

# Compute dot product of tones and training data
X_train_sin = np.dot(X_train, sin_tones.T)
X_train_cos = np.dot(X_train, cos_tones.T)
X_test_sin = np.dot(X_test, sin_tones.T)
X_test_cos = np.dot(X_test, cos_tones.T)
# print(X_train_sin.dtype)

# Power of tones
pow_train = X_train_cos**2 + X_train_sin**2
pow_test = X_test_cos**2 + X_test_sin**2
# print(pow_train.shape)
# print(pow_train.dtype)
# print(pow_train[0])

# Normalize power
max_val = np.max(pow_train, axis=1)
pow_train = pow_train / max_val[:, None]

max_val = np.max(pow_test, axis=1)
pow_test = pow_test / max_val[:, None]

# Convert power to dB
pow_train = 10 * np.log10(pow_train)
pow_test = 10 * np.log10(pow_test)


# Clip to -40
pow_train = np.where(pow_train < -40, -40, pow_train)
pow_test = np.where(pow_test < -40, -40, pow_test)
print(pow_train.shape)

# for i in range(16):
#     # plt.bar(freqs, pow_train[i*101], width=3, color='b')
#     plt.plot(freqs, pow_train[i*100], 'ro-')
#     plt.grid(True)
#     plt.title("Power of tones for " + characters[i])
#     plt.xlabel("Frequency (Hz)")
#     plt.ylabel("Power")
#     plt.savefig("TS_plots/dtmf_" + characters[i] + ".png")
#     plt.close()
#     # plt.show()


# Shuffle training data and convert to float
train_data = np.hstack((pow_train, y_train))
np.random.shuffle(train_data)
# print(train_data[0])
X_train = train_data[:, :-1]
y_train = train_data[:, -1]
# X_train = X_train.astype(float)
# y_train = y_train.astype(float)
# print(X_train.dtype)
# print(X_train.shape)

# Create validation data
cutoff1 = int( 0.60 * len(X_train) )
cutoff2 = int( 0.80 * len(X_train) )
X_val = X_train[cutoff1:cutoff2, :]
y_val = y_train[cutoff1:cutoff2]
X_train = X_train[:cutoff1, :]
y_train = y_train[:cutoff1]

# print(X_train.dtype)
# print(X_val.shape)

# Shuffle test data and convert to float
test_data = np.hstack((pow_test, y_test))
np.random.shuffle(test_data)
X_test = test_data[:, :-1]
y_test = test_data[:, -1]
# X_test = X_test.astype(float)
# y_test = y_test.astype(float)

# Design a simple neural network 
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(512, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(16, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=25, validation_data=(X_val, y_val))

# Evaluate the model
actual = y_test
predictions = model.predict(X_test)
predictions = np.argmax(predictions, axis=1)
# print("Predictions: ", predictions)

# Confusion matrix
confusion_matrix = tf.math.confusion_matrix(actual, predictions)
print("Confusion matrix: ", confusion_matrix)

# Accuracy
accuracy = np.sum(np.diag(confusion_matrix)) / np.sum(confusion_matrix)
print("Accuracy: ", accuracy)