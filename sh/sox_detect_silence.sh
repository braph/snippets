#!/bin/bash

unset CDPATH
set -u
set +o histexpand

TEST_TIME=3

while :; do
   parec -d alsa_output.pci-0000_00_1b.0.analog-stereo.monitor |\
      sox -t raw -r 44100 -L -e signed-integer -b 16 -c 2 - -p \
      trim 0 $TEST_TIME \
      silence 1 2.00 0.1% \
      stat

   sleep 1
done
