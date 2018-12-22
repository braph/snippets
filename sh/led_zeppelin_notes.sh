#!/bin/bash

unset CDPATH
set -u
set +o histexpand

sleep 3

x=( 1.E 1.C 1.C 1.D 1.E 1.E 1.E 1.F# 1.A 1.G 1.F# 1.G 1.G 1.G 1.G 1.A 1.A 1.E 1.A 1.G 1.G 1.F# 1.E 1.D 1.A 2.C 1.B 2.C 2.D 2.E 2.D 1.G 1.A 1.A )
x=( 1.E 1.A 1.G 1.G 1.F# 1.E 1.D 1.A 2.C 1.B 2.C 2.D 2.E 2.D 1.G 1.A 1.A )

clear;
for n in "${x[@]}"; do
   figlet -f big "$n"
   sleep 1;
   clear
   sleep 0.3;
done

