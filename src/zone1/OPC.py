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

while 1:
    if time.time()%60 == 0:
        break


t = time.time()

while 1:
    while time.time() - t < 1:
        continue
    t = time.time()
    #Do Something

    #Get register values. Some from field. Some from ISA above
    l1 = field_client.read_holding_registers(L1, 1).registers[0]
    l2 = isa_client.read_holding_registers(L2, 1).registers[0]
    t1 = field_client.read_holding_registers(T1, 1).registers[0]
    t2 = isa_client.read_holding_registers(T2, 1).registers[0]
    v1 = isa_client.read_holding_registers(V1, 1).registers[0]
    v2 = field_client.read_holding_registers(V2, 1).registers[0]
    p  = isa_client.read_holding_registers( P, 1).registers[0]
    f1 = isa_client.read_holding_registers(F1, 1).registers[0]
    f2 = field_client.read_holding_registers(F2, 1).registers[0]
    f3 = isa_client.read_holding_registers(F3, 1).registers[0]
    h  = field_client.read_holding_registers( H, 1).registers[0]

    if l1 > 85:
        v2 = 0
    
    if l1 < 50:
        v2 = 1

    if l2 > 85:
        v2 = 1
    
    if l2 < 50:
        v2 = 0

    if t1 > 90:
        v2 = 1
        h = 0

    if t1 < 60:
        v2 = 0
        h = 1

    if t2 > 90:
        v2 = 1

    if t2 < 60:
        v2 = 0


    #write values to isa registers
    isa_client.write_register(L1, l1)
    isa_client.write_register(T1, t1)
    isa_client.write_register(V2, v2)
    isa_client.write_register(F2, f2)
    isa_client.write_register( H,  h)