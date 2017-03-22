#!/usr/bin/python
#MTU Server
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time
import numpy as np
import logging
from sklearn.decomposition import PCA
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

Data = []
pca = PCA(n_components = 3)
Data = np.load("data.npy")
pca.fit(Data)
print "PCA Built"
t = time.time()
i = 0
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
y = []
def update(i):
    #Read registers from the specific zone
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

    v = np.array([[l1, l2, t1, t2, v1, v2, p, f1, f2, f3, h]])
    v_transform = pca.transform(v)
    y.append(v_transform[0])
    x = range(len(y))
    ax.clear()
    ax.set_title("PCA Based Prediction (Top 3 Scores).")
    ax.set_ylabel("Top 3 scores")
    ax.set_xlabel("Evaluation Points")
    ax.set_xlim([0, 1.33*len(y)])
    ax.plot(x, y)

a = anim.FuncAnimation(fig, update, frames=100000, repeat=False)
plt.show()