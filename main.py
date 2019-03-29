#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
from influxdb import InfluxDBClient
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

client = InfluxDBClient(host='localhost', port='8086')
client.switch_database('multimeter')

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.wake()

def read():
	ina.configure(ina.RANGE_16V)
	bus = ina.voltage()
	cur = ina.current()
	shunt = ina.shunt_voltage()
	power = ina.power()

	print("Bus Voltage: %.3f V" % bus)
	try:
		print("Bus Current: %.3f mA" % cur)
		print("Power: %.3f mW" % power)
		print("Shunt voltage: %.3f mV" % shunt)
		print("")
	except DeviceRangeError as e:
# Current out of device range with specified shunt resister
		print(e)
	json = [{
		"measurement": "data",
		"fields": {
			"busVoltage": bus,
			"current": cur,
			"power": power,
			"shuntVoltage": shunt,
		}
	}]

	client.write_points(json)

if __name__ == "__main__":
	while True:
		read()
		#ina.sleep()
		time.sleep(60)
		#ina.wake()
