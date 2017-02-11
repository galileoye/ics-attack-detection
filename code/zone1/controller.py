#RTU Server
from pymodbus.server.sync import StartTcpServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

store = ModbusSlaveContext(di = ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)
identity = ModbusDeviceIdentification()

StartTcpServer(context, identity=identity, address=("10.0.6.11", 6060))
