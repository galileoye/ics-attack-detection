#!/usr/bin/python
#MTU Server
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

field_client = ModbusTcpClient(FIELD_IP, FIELD_PORT)
field_client.connect()
isa_client = ModbusTcpClient(OPC1_IP, OPC1_PORT)
isa_client.connect()

# while 1:
#     now = time.time()
#     print (int(now)/60)%60
#     if (int(now)/60)%60 == 0:
#         print "starting connection"
#         break



t = time.time()

while 1:
    while time.time() - t < 0.2:
        continue
    t = time.time()
    #Do Something

    #Get register values. Some from field. Some from ISA above
    l1 = float(field_client.read_holding_registers(L1, 1).registers[0])
    l2 = float(isa_client.read_holding_registers(L2, 1).registers[0])
    t1 = float(field_client.read_holding_registers(T1, 1).registers[0])
    t2 = float(isa_client.read_holding_registers(T2, 1).registers[0])
    v1 = isa_client.read_holding_registers(V1, 1).registers[0]
    v2 = field_client.read_holding_registers(V2, 1).registers[0]
    p  = isa_client.read_holding_registers( P, 1).registers[0]
    f1 = isa_client.read_holding_registers(F1, 1).registers[0]
    f2 = field_client.read_holding_registers(F2, 1).registers[0]
    f3 = isa_client.read_holding_registers(F3, 1).registers[0]
    h  = field_client.read_holding_registers( H, 1).registers[0]

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



    #write values to isa registers
    isa_client.write_register(L1, l1)
    isa_client.write_register(T1, t1)
    isa_client.write_register(V2, v2)
    isa_client.write_register(F2, f2)
    isa_client.write_register( H,  h)

    field_client.write_register(V2, v2)
    field_client.write_register( H,  h)


    print(
        "L1 ",l1,",",
        "L2 ",l2,",",
        "T1 ",t1,",",
        "T2 ",t2,",",
        "V1 ",v1,",",
        "V2 ",v2,",",
        "P  ",p,",",
        "F1 ",f1,",",
        "F2 ",f2,",",
        "F3 ",f3,",",
        "H  ",h,",",
        "\n"
    )