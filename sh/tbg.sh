#!/bin/bash

unset CDPATH
set -u +o histexpand

BIN=$0

if (( $# == 2 )); then
   tmux move-window -d -s "$1" -t "$2"
elif (( $# == 1 )); then
   tmux choose-tree -u -b "run-shell \"$BIN $1 %%\"" -c ''
else
   tmux choose-tree -u -c "run-shell \"$BIN %%\"" -b 'run-shell "true"'
fi


