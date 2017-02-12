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

t = time.time()

while 1:
    while time.time() - t < 1:
        continue
    t = time.time()
    #Do Something