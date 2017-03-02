#!/usr/bin/python
#MTU Server
from config import *
from pymodbus.client.sync import ModbusTcpClient
import time
import signal
import sys
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

x = 0
class S:
    cnt = 0

    def __call__(self, signum, frame):
        if (self.cnt == 1):
            sys.exit()
        self.cnt += 1
        self.signal_handler()
        
    def signal_handler(self):
        print('You pressed Ctrl+C!')
        fake_client = ModbusTcpClient(FAKE_FIELD_IP, FAKE_FIELD_PORT)
        fake_client.connect()
        t = time.time()
        while True:
            while time.time() - t < 0.2:
                continue
            t = time.time()
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

            isa_client.write_register(L2, l2)
            isa_client.write_register(T2, t2)
            isa_client.write_register(V1, v1)
            isa_client.write_register( P,  p)
            isa_client.write_register(F1, f1)
            isa_client.write_register(F3, f3)
            print(
                "compromised_zone2",",",
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


signal.signal(signal.SIGINT, S())


t = time.time()
T = time.time()
while 1:
    while time.time() - t < 0.2:
        continue
    t = time.time()
    #Do Something

    #Get register values. Some from field. Some from ISA above
    l1 = float(isa_client.read_holding_registers(L1, 1).registers[0])
    l2 = float(field_client.read_holding_registers(L2, 1).registers[0])
    t1 = float(isa_client.read_holding_registers(T1, 1).registers[0])
    t2 = float(field_client.read_holding_registers(T2, 1).registers[0])
    v1 = field_client.read_holding_registers(V1, 1).registers[0]
    v2 = isa_client.read_holding_registers(V2, 1).registers[0]
    p  = field_client.read_holding_registers( P, 1).registers[0]
    f1 = field_client.read_holding_registers(F1, 1).registers[0]
    f2 = isa_client.read_holding_registers(F2, 1).registers[0]
    f3 = field_client.read_holding_registers(F3, 1).registers[0]
    h  = isa_client.read_holding_registers( H, 1).registers[0]


    #Contro p and v1
    if l1 > 85 and l2 < 50:
        v1 = 1
        p = 1
        # if t1 > 90 and t2 > 90:
        #     v1 = 1
        #     p = 1
            
        # if t1 < 60 and t2 > 90:
        #     v1 = 1
        #     p  = 1

        # if t1 > 90 and t2 < 60:
        #     v1 = 1
        #     p  = 1
        
        # if t1 < 60 and t2 < 60:
        #     v1 = 1
        #     p = 1

    if l1 < 50 and l2 > 85:
        v1 = 0
        p = 0
        # if t1 > 90 and t2 > 90:
        #     v1 = 0
        #     p = 0
            
        # if t1 < 60 and t2 > 90:
        #     v1 = 0
        #     p  = 0

        # if t1 > 90 and t2 < 60:
        #     v1 = 0
        #     p  = 0
        
        # if t1 < 60 and t2 < 60:
        #     v1 = 0
        #     p = 0
    
        

    #write values to isa registers
    isa_client.write_register(L2, l2)
    isa_client.write_register(T2, t2)
    isa_client.write_register(V1, v1)
    isa_client.write_register( P,  p)
    isa_client.write_register(F1, f1)
    isa_client.write_register(F3, f3)
    
    field_client.write_register(V1, v1)
    field_client.write_register( P,  p)
    
    
    print(
        "zone2",",",
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

