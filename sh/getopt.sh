#!/bin/bash

unset CDPATH
set -u +o histexpand

while getopts ":n:t:" options; do
   case "${options}" in
      n) NAME=${OPTARG}
         ;;
      t)
         ;;
      :)
         echo "Error: -${OPTARG} requires an argument."
         exit 1 ;;
      *) exit 1 ;;
   esac
done
