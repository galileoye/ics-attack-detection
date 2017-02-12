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
    