#!/usr/bin/env python

# 2018 / MIT / Tim Clem / github.com/misterfifths
# See LICENSE for details
# 
# Domoticz update script for SGP30 Airquality sensor
# You have to add 2 Dummy sensors in Domoticz
# For CO2 type 'Air Quality'
# For VOC type 'Custom Sensor'
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor

from __future__ import print_function

from time import sleep
from sgp30 import SGP30
from smbus import SMBus
import requests

DOMOTICZ_IP = 'http://127.0.0.1:8080'
DEVICE_IDX_CO = '2'
DEVICE_IDX_VOC = '3'

def main():
    smbus = SMBus(1)  # zero on some boards
    warming_up = True
    baseline_counter = 0

    with SGP30(smbus) as chip:
        while True:
            measurement = chip.measure_air_quality()

            # Chip returns (400, 0) for the first ~15 seconds while it warms up
            if warming_up:
                if measurement.is_probably_warmup_value():
                    print('... warming up ...')
                    sleep(1)
                    continue
                else:
                    warming_up = False

            print(measurement)

	    # Domoticz update script
	    # CO2 update to Domoticz
	    requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + DEVICE_IDX_CO + "&nvalue=" + str(measurement[1]))
	    # print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + DEVICE_IDX_CO + "&nvalue=" +  str(measurement[1]))
	    # VOC update to Domoticz
	    requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + DEVICE_IDX_VOC + "&nvalue=0&svalue=" + str(measurement[2]))
	    # print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + DEVICE_IDX_VOC + "&nvalue=0&svalue=" + str(measurement[2]))

            # Don't take this as a complete example... read the spec sheet about how you're supposed to stash and restore the baseline, initial burn-in, humidity compensation, *and how you need to sample every second to maintain accurate results*
            baseline_counter = baseline_counter + 1
            if baseline_counter % 100 == 0:
                baseline_counter = 0
                baseline = chip.get_baseline()
                print('>> Baseline:', baseline)

            sleep(1)

if __name__ == '__main__':
    main()
