import sys
import os
import wave
import random
import numpy as np
import tensorflow as tf

filedir = "../stacked_sets/"
characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "pound", "star"]

# Create a dictionary of training and test files
TS = {character: filedir + "ts_" + character + ".dat" for character in characters}
TEST = {character: filedir + "test_" + character + ".dat" for character in characters}

# Read tones and create labels
X_train = np.empty((0, 512), dtype=np.uint16)
y_train = np.empty((0, 1), dtype=int)
X_test = np.empty((0, 512), dtype=np.uint16)
y_test = np.empty((0, 1), dtype=int)
label = 0
for keys in TS.keys():
    f = open(TS[keys], "rb")
    g = open(TEST[keys], "rb")
    while True:
        # Read training data
        atone = np.fromfile(f, np.uint16, 512)
        if atone.size < 512:
            break
        X_train = np.vstack((X_train, atone))
        # Read test data
        atone = np.fromfile(g, np.uint16, 512)
        if atone.size < 512:
            break
        X_test = np.vstack((X_test, atone))
    f.close()
    g.close()
    num_ts_tones = X_train.shape[0] - y_train.shape[0]
    y_train = np.vstack((y_train, np.full((num_ts_tones, 1), label)))
    num_test_tones = X_test.shape[0] - y_test.shape[0]
    y_test = np.vstack((y_test, np.full((num_test_tones, 1), label)))
    label += 1
print(X_train.shape)
# Preprocessing the data
# Generate pure tones
N = 512
freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
pure_tones = np.zeros((0, N), dtype=np.uint16)
d = len(freqs)
A = np.zeros((d, N))
fs = 16000
n = np.arange(N)/fs
for freq in freqs:
    cos_tone = 10000 * np.cos(2 * np.pi * freq * n)
    sin_tone = 10000 * np.sin(2 * np.pi * freq * n)
    pure_tones = np.vstack((pure_tones, cos_tone))
    pure_tones = np.vstack((pure_tones, sin_tone))
# print(pure_tones.shape)

# Dot product of pure tones and training data
X_train = np.matmul(X_train, pure_tones.T)
X_test = np.matmul(X_test, pure_tones.T)
# print(X_train.shape)
# print(X_test.shape)

# Shuffle training data and convert to float
train_data = np.hstack((X_train, y_train))
np.random.shuffle(train_data)
X_train = train_data[:, :-1]
y_train = train_data[:, -1]
X_train = X_train.astype(float)
y_train = y_train.astype(float)

# Create validation data
X_val = X_train[:600, :]
y_val = y_train[:600]

# Shuffle test data and convert to float
test_data = np.hstack((X_test, y_test))
np.random.shuffle(test_data)
X_test = test_data[:, :-1]
y_test = test_data[:, -1]
X_test = X_test.astype(float)
y_test = y_test.astype(float)


# Design a simple neural network with 4 hidden layers
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(512, activation='relu', input_shape=(16,)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(16, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, validation_data=(X_val, y_val))

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