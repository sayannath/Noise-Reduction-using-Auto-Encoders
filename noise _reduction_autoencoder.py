# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13ODqY2zh4ic2cZUPKjRRdn8XxCyBqqjf

# MNIST Dataset

## Import Libraries
"""

import os
import numpy as np
import matplotlib.pyplot as plt

import tensorflow
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Sequential

"""## Loading the Dataset"""

(x_train, _), (x_test, _) = mnist.load_data()

"""## Splitting the Dataset"""

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

"""## Adding the Noise"""

noise_factor = 0.5
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape) 
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape) 

x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

"""## Displaying the Noisy Images"""

#Displaying images with noise
plt.figure(figsize=(20, 2))
for i in range(1,10):
    ax = plt.subplot(1, 10, i)
    plt.imshow(x_test_noisy[i].reshape(28, 28), cmap="binary")
plt.show()

"""## Creating the model"""

model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
 

model.add(MaxPooling2D((2, 2), padding='same'))
 
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(1, (3, 3), activation='relu', padding='same'))

"""## Compiling the Model"""

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

"""## Summary of the Model"""

model.summary()

"""## Training the Model"""

model.fit(x_train_noisy, x_train, epochs=25, batch_size=256, shuffle=True, 
          validation_data=(x_test_noisy, x_test))

"""## Evaluating the Model"""

model.evaluate(x_test_noisy, x_test)

"""The Accuracy of the Model is 80.77%
The Loss of the Model is 2.10%

## Saving the Model
"""

model.save('denoising_autoencoder.model')

"""## Predicting the Model"""

no_noise_img = model.predict(x_test_noisy)

plt.figure(figsize=(40, 4))
for i in range(10):
    # display original
    ax = plt.subplot(3, 20, i + 1)
    plt.imshow(x_test_noisy[i].reshape(28, 28), cmap="binary")
    
    # display reconstructed (after noise removed) image
    ax = plt.subplot(3, 20, 40 +i+ 1)
    plt.imshow(no_noise_img[i].reshape(28, 28), cmap="binary")

plt.show()

"""# Getting the File Size"""

def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size

def convert_bytes(size, unit=None):
    if unit == "KB":
        return print('File Size: ' + str(round(size/1024, 3)) + 'Kilobytes')
    elif unit == 'MB':
        return print('File Size: ' + str(round(size/(1024*1024), 3)) + 'Megabytes')
    else:
        return print('File Size: ' + str(size) + 'bytes')

"""## Saving the model in Keras format"""

KERAS_FILE = 'denoise_model.h5'
model.save(KERAS_FILE)

"""## Saving the model in TF Lite format"""

TF_LITE_MODEL = 'denoise_model.tflite'

tf_lite_converter = tensorflow.lite.TFLiteConverter.from_keras_model(model)
tflite_model = tf_lite_converter.convert()

tflite_model_name = TF_LITE_MODEL
open(tflite_model_name, "wb").write(tflite_model)

"""### Getting the size of Keras File"""

convert_bytes(get_file_size(KERAS_FILE), "KB")

"""### Getting the size of TF Lite File"""

convert_bytes(get_file_size(TF_LITE_MODEL), "KB")

