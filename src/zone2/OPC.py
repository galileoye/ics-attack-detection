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
isa_client = ModbusTcpClient(OPC2_IP, OPC2_PORT)
isa_client.connect()

# while 1:
#     now = time.time()
#     print (int(now)/60)%60
#     if (int(now)/60)%60 == 0:
#         print "starting connection"
#         break



t = time.time()

while 1:
    while time.time() - t < 1:
        continue
    t = time.time()
    #Do Something

    #Get register values. Some from field. Some from ISA above
    l1 = isa_client.read_holding_registers(L1, 1).registers[0]
    l2 = field_client.read_holding_registers(L2, 1).registers[0]
    t1 = isa_client.read_holding_registers(T1, 1).registers[0]
    t2 = field_client.read_holding_registers(T2, 1).registers[0]
    v1 = field_client.read_holding_registers(V1, 1).registers[0]
    v2 = isa_client.read_holding_registers(V2, 1).registers[0]
    p  = field_client.read_holding_registers( P, 1).registers[0]
    f1 = field_client.read_holding_registers(F1, 1).registers[0]
    f2 = isa_client.read_holding_registers(F2, 1).registers[0]
    f3 = field_client.read_holding_registers(F3, 1).registers[0]
    h  = isa_client.read_holding_registers( H, 1).registers[0]


    if l1 > 85:
        p = 1
        v1 = 1
    
    if l1 < 50:
        p = 0
        v1 = 0

    if l2 > 85:
        v1 = 0
        p = 0
    
    if l2 < 50:
        p = 1
        v1 = 1

    if t1 > 90:
        p = 1
        v1 = 1

    if t1 < 60:
        v1 = 0
        p = 0

    if t2 > 90:
        v1 = 0
        p = 0

    if t2 < 60:
        p = 1
        v1 = 1
        

    #write values to isa registers
    isa_client.write_register(L2, l2)
    isa_client.write_register(T2, t2)
    isa_client.write_register(V1, v1)
    isa_client.write_register( P,  p)
    isa_client.write_register(F1, f1)
    isa_client.write_register(F3, f3)
    
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