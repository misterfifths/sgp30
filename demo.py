#!/usr/bin/env python

# MIT; see LICENSE

from __future__ import print_function

from time import sleep
from sgp30 import SGP30


def main():
    baseline_counter = 0
    with SGP30() as chip:
        while True:
            measurement = chip.measure_air_quality()

            # Chip returns (400, 0) for the first ~15 seconds while it warms up
            if not measurement.is_probably_valid():
                print('... warming up ...')
                sleep(1)
                continue

            print(measurement)

            # Don't take this as a complete example... read the spec sheet about how you're supposed to stash and restore this baseline, and initial burn-in, and so on.
            baseline_counter = baseline_counter + 1
            if baseline_counter % 100 == 0:
                baseline_counter = 0
                baseline = chip.get_baseline()
                print('>> Baseline:', baseline)

            sleep(1)

if __name__ == '__main__':
    main()
