#!/usr/bin/python
#MTU Server
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

opc1_client = ModbusTcpClient(OPC1_IP, OPC1_PORT)
opc1_client.connect()
opc2_client = ModbusTcpClient(OPC2_IP, OPC2_PORT)
opc2_client.connect()

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
while 1:
    if time.time() - T > SIM_TIME:
        break
    while time.time() - t < 2*SIM_STEP:
        continue
    t = time.time()

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
    
    #printvalues("isa", l1, l2, t1, t2, v1, v2, p, f1, f2, f3, h)

    #Write to the register of the other zone
    opc2_client.write_register(L1, l1)
    opc1_client.write_register(L2, l2)
    opc2_client.write_register(T1, t1)
    opc1_client.write_register(T2, t2)
    opc1_client.write_register(V1, v1)
    opc2_client.write_register(V2, v2)
    opc1_client.write_register( P,  p)
    opc1_client.write_register(F1, f1)
    opc2_client.write_register(F2, f2)
    opc1_client.write_register(F3, f3)
    opc2_client.write_register( H,  h)
