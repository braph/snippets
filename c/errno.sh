#!/bin/dash

ERROR_VAR='ERRORS'
MAX=$(errno -l | cut -d' ' -f2 | sort -n | tail -1)

echo "const * char $ERROR_VAR[$MAX];"

#errno -l | sed -r 's/([A-Z0-9]+) ([0-9]+).*/\2 \1/g' | sort -n | while read n e
errno -l | sort -n -k 2 | while read NAME NUM _
do
   echo "$ERROR_VAR[$NUM] = \"$NAME\";"
done
