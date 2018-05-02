#!/usr/bin/env python

# 2018 / MIT / Tim Clem / github.com/misterfifths
# See LICENSE for details

from __future__ import print_function

from time import sleep
from sgp30 import SGP30
from smbus import SMBus


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

            # Don't take this as a complete example... read the spec sheet about how you're supposed to stash and restore the baseline, initial burn-in, humidity compensation, *and how you need to sample every second to maintain accurate results*
            baseline_counter = baseline_counter + 1
            if baseline_counter % 100 == 0:
                baseline_counter = 0
                baseline = chip.get_baseline()
                print('>> Baseline:', baseline)

            sleep(1)

if __name__ == '__main__':
    main()
