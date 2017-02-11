#MTU Server
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

#Process Variables
L1  = 0
L2  = 1
T1  = 2
T2  = 3
F1  = 4
F2  = 5
F3  = 6
F4  = 7
F5  = 9

#Auto Variables
V1  = 10
V2  = 11
H   = 12

zone1_client = ModbusTcpClient(ZONE1_CONTROLLER_IP, ZONE1_CONTROLLER_PORT)
zone1_client.connect()
zone2_client = ModbusTcpClient(ZONE2_CONTROLLER_IP, ZONE2_CONTROLLER_PORT)
zone2_client.connect()

t = time.time()

while 1:
    while time.time() - t < 1:
        continue
    t = time.time()
    #Do Something