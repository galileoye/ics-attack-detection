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

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

opc1_client = ModbusTcpClient(OPC1_IP, OPC1_PORT)
opc1_client.connect()
opc2_client = ModbusTcpClient(OPC2_IP, OPC2_PORT)
opc2_client.connect()

t = time.time()
seq = 50
Data = []
Data = np.load("data.npy")
X = []
for i in range(Data.shape[0]-seq-10):
    t = 0
    tmp = []
    while t < seq:
        tmp.append(Data[t + i])
        t += 1
    X.append(tmp)
# X = Data
X = np.array(X)
print X
Y = [1 for i in range(X.shape[0])]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

print X.shape

batch_size = 64
nb_classes = 1
nb_epoch = 5

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

model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model_json = model.to_json()
with open("model.json","w") as json_file:
    json_file.write(model_json)
model.save_weights("model_weights.h5")
print("Saved the Model to Disk")

json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("model_weights.h5")
t = time.time()
x = []
while True:
    while time.time()-t < 0.1:
        continue
    t = time.time()
    l1 = float(opc1_client.read_holding_registers(L1, 1).registers[0])
    l2 = float(opc2_client.read_holding_registers(L2, 1).registers[0])
    t1 = float(opc1_client.read_holding_registers(T1, 1).registers[0])
    t2 = float(opc2_client.read_holding_registers(T2, 1).registers[0])
    v1 = opc2_client.read_holding_registers(V1, 1).registers[0]
    v2 = opc1_client.read_holding_registers(V2, 1).registers[0]
    p  = opc2_client.read_holding_registers( P, 1).registers[0]
    f1 = opc2_client.read_holding_registers(F1, 1).registers[0]
    f2 = opc1_client.read_holding_registers(F2, 1).registers[0]
    f3 = opc2_client.read_holding_registers(F3, 1).registers[0]
    h  = opc1_client.read_holding_registers( H, 1).registers[0]

    v = [l1, l2, t1, t2, v1, v2, p, f1, f2, f3, h]
    x.append(v)
    if len(x) == seq:
        x = np.array([x])
        print model.predict(x, batch_size=1, verbose=0)
        x = []