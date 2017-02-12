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
client.write_register(T2, 0)
client.write_register(V1, 0)
client.write_register(V2, 0)
client.write_register( P, 0)
client.write_register(F1, 0)
client.write_register(F2, 0)
client.write_register(F3, 0)
client.write_register( H, 1)



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

    