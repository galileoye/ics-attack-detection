#RTU Client
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

client = ModbusTcpClient(FIELD_IP, FIELD_PORT)
client.connect()

# Initialize Registers Here
client.write_register(L1, 90)
client.write_register(L2, 40)
client.write_register(T1, 95)
client.write_register(T2, 50)
client.write_register(V1, 0)
client.write_register(V2, 0)
client.write_register( P, 0)
client.write_register(F1, 0)
client.write_register(F2, 0)
client.write_register(F3, 0)
client.write_register( H, 1)

while 1:
    if time.time()%60 == 0:
        break


t = time.time()

while True:
    while time.time() - t < 1:
        continue
    # Do something here
    l1 = client.read_holding_registers(L1, 1).registers[0]
    l2 = client.read_holding_registers(L2, 1).registers[0]
    t1 = client.read_holding_registers(T1, 1).registers[0]
    t2 = client.read_holding_registers(T2, 1).registers[0]
    v1 = client.read_holding_registers(V1, 1).registers[0]
    v2 = client.read_holding_registers(V2, 1).registers[0]
    p  = client.read_holding_registers( P, 1).registers[0]
    f1 = client.read_holding_registers(F1, 1).registers[0]
    f2 = client.read_holding_registers(F2, 1).registers[0]
    f3 = client.read_holding_registers(F3, 1).registers[0]
    h  = client.read_holding_registers( H, 1).registers[0]

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
    if h == 1:
        t1 = t1 + heat_coefficient/l1
    
    if h == 0:
        t1 = t1 - 1
    
    if f1 == 1:
        l1 = l1 - 1
        l2 = l2 + 1
        t2 = t2 + (1/l2)(t1 - t2)

    if f2 == 1:
        l1 = l1 + 1
        l2 = l2 - 1
        t1 = t1 + (1/l1)(t2 - t1)

    client.write_register(L1, l1)
    client.write_register(L2, l2)
    client.write_register(T1, t1)
    client.write_register(T2, t2)
    client.write_register(V1, v1)
    client.write_register(V2, v2)
    client.write_register( P,  p)
    client.write_register(F1, f1)
    client.write_register(F2, f2)
    client.write_register(F3, f3)
    client.write_register( H,  h)