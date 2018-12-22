#!/bin/bash

unset CDPATH
set -u +o histexpand

enable_inputs() {
   echo 'enable inputs'
   xinput --enable 13
   xinput --enable 18
}

disable_inputs() {
   xinput --disable 13
   xinput --disable 18
}

trap 'enable_inputs' 0

disable_inputs

xdotool search --onlyvisible --name Breitbandmessung windowactivate
sleep 1
xdotool mousemove 332 332
sleep 1
xdotool click 1
sleep 1
xdotool mousemove 978 625
sleep 5
xdotool click 1

enable_inputs
