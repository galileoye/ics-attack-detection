#!/usr/bin/python
#RTU Client
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

fake_client = ModbusTcpClient(FAKE_FIELD_IP, FAKE_FIELD_PORT)
fake_client.connect()

# Initialize Registers Here
fake_client.write_register(L1, 90.0)
fake_client.write_register(L2, 40.0)
fake_client.write_register(T1, 95.0)
fake_client.write_register(T2, 50.0)
fake_client.write_register(V1, 0.0)
fake_client.write_register(V2, 0.0)
fake_client.write_register( P, 0.0)
fake_client.write_register(F1, 0.0)
fake_client.write_register(F2, 0.0)
fake_client.write_register(F3, 0.0)
fake_client.write_register( H, 1.0)

l1 = 90


# while 1:
#     then = time.time()
#     now = time.time()
#     diff = int(now-then)
#     m, s = diff//60, diff%60
#     print s
#     if s == 0:
#         print "starting connection"
#         break
print "Simulation will start when the time is 0, 25, 50 ,75"
to = 0
while 1:
    toot = int(time.time())%100
    if to == toot - 1:
        print toot
    to = toot
    # print to
    if to == 0 or to == 25 or to == 50 or to == 75:
        break
    

t = time.time()
T = time.time()
tmp = time.time()
while True:

    if time.time() - tmp > SIM_TIME:
        break
    
    while time.time() - t < 0.1:
        continue

    t = time.time()
    # Do something here
    l1 = float(fake_client.read_holding_registers(L1, 1).registers[0])
    l2 = float(fake_client.read_holding_registers(L2, 1).registers[0])
    t1 = float(fake_client.read_holding_registers(T1, 1).registers[0])
    t2 = float(fake_client.read_holding_registers(T2, 1).registers[0])
    v1 = fake_client.read_holding_registers(V1, 1).registers[0]
    v2 = fake_client.read_holding_registers(V2, 1).registers[0]
    p  = fake_client.read_holding_registers( P, 1).registers[0]
    f1 = fake_client.read_holding_registers(F1, 1).registers[0]
    f2 = fake_client.read_holding_registers(F2, 1).registers[0]
    f3 = fake_client.read_holding_registers(F3, 1).registers[0]
    h  = fake_client.read_holding_registers( H, 1).registers[0]
    if time.time() - T > 0.2:
        T = time.time()
        # Control v2 and h
        if l1 > 85 and l2 < 50:
            if t1 > 90 and t2 > 90:
                v2 = 0
                h = 0
                
            if t1 < 60 and t2 > 90:
                v2 = 0
                h  = 1

            if t1 > 90 and t2 < 60:
                v2 = 0
                h  = 1
            
            if t1 < 60 and t2 < 60:
                v2 = 0
                h = 1
            
        if l1 < 50 and l2 > 85:
            if t1 > 90 and t2 > 90:
                v2 = 1
                h = 0
                
            if t1 < 60 and t2 > 90:
                v2 = 1
                h  = 0

            if t1 > 90 and t2 < 60:
                v2 = 1
                h  = 0
            
            if t1 < 60 and t2 < 60:
                v2 = 1
                h = 1

        if l1 > 85 and l2 < 50:
            v1 = 1
            p = 1

        if l1 < 50 and l2 > 85:
            v1 = 0
            p = 0
            

    
    
    #Set process variables
    if v1 == 1 and p == 1:
        f1 = 1
        f3 = 0
    
    if p == 0:
        f1 = 0
        f3 = 0
    
    if v1 == 0 and p == 1:
        f1 = 0
        f3 = 1

    if v2 == 1:
        f2 = 1

    if v2 == 0:
        f2 = 0

    #compute process variables
    # t2 = t2 - (1.0*heat_coefficient)/(1.0*l1)
    if h == 1:
        if l1 > 0:
            t1 = t1 + (1.0*heat_coefficient_2)/(1.0*l1)
    
    if h == 0:
        if l1 > 0:
            t1 = t1 - (1.0*heat_coefficient)/(1.0*l1)
    
    if f1 == 1:
        if l1 > 0:
            l1 = l1 - 1.0
        l2 = l2 + 1.0
        if l2>0:
            t2 = t2 + (1.0/l2)*(t1 - t2)

    if f2 == 1:
        l1 = l1 + 1.0
        if l2 > 0:
            l2 = l2 - 1.0
        if l1 > 0:
            t1 = t1 + (1.0/l1)*(t2 - t1)

    fake_client.write_register(L1, l1)
    fake_client.write_register(L2, l2)
    fake_client.write_register(T1, t1)
    fake_client.write_register(T2, t2)
    fake_client.write_register(F1, f1)
    fake_client.write_register(F2, f2)
    fake_client.write_register(F3, f3)
    fake_client.write_register(V1, v1)
    fake_client.write_register(V2, v2)
    fake_client.write_register(P, p)
    fake_client.write_register(H, h)

    #printvalues("fake field", l1, l2, t1, t2, v1, v2, p, f1, f2, f3, h)
    