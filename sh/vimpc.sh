#!/bin/bash

unset CDPATH
set -u
set +o histexpand

HOST=10.0.0.10

mpc -h "$HOST" playlist -f '%position% %artist% - %album% - %title%' |\
   vim \
   "+set nonumber" \
   "+map p :exe '!mpc -h $HOST play ' . substitute(getline('.'), ' .*', '', '')<CR>" \
   -
