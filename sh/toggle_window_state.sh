#!/bin/bash
myid=$(ps $(xdotool getwindowfocus getwindowpid) |tail -n 1 |awk ‘{print $3}’)
if [[ $myid == “Sl” ]]
then
   kill -STOP `xdotool getwindowfocus getwindowpid`
else
   kill -CONT `xdotool getwindowfocus getwindowpid`
fi
