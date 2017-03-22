#!/usr/bin/python
#MTU Server

import os
os.environ['KERAS_BACKEND'] = 'theano'
# os.environ['THEANO_FLAGS'] = 'floatX=float32,device=gpu,lib.cnmem=0.8,dnn.conv.algo_bwd_filter=deterministic,dnn.conv.algo_bwd_data=deterministic,blas.ldflags=-LC:/toolkits/openblas-0.2.14-int32/bin -lopenblas'
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time
import numpy as np
import logging
from sklearn.cross_validation import train_test_split


from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

import matplotlib.pyplot as plt
import matplotlib.animation as anim

Data = []
Data = np.load("data.npy")
X = []
for i in range(Data.shape[0]-seq-padding):
    t = padding
    tmp = []
    while t < seq + padding:
        tmp.append(Data[t + i])
        t += 1
    X.append(tmp)

X = np.array(X)
print X
Y = [1 for i in range(X.shape[0])]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

print X.shape

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
model = Sequential()

model.add(LSTM(100, input_shape = (seq, 11)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

model.fit(
    X_train, 
    Y_train, 
    batch_size=batch_size, 
    nb_epoch=nb_epoch,
    verbose=1, 
    validation_data=(X_test, Y_test)
    )
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model_json = model.to_json()
with open("model.json","w") as json_file:
    json_file.write(model_json)
model.save_weights("model_weights.h5", overwrite=True)
print("Saved the Model to Disk")
