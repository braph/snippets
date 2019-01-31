#!/bin/dash

ERROR_VAR=${1:-'ERRORS'}
MAX=$(errno -l | cut -d' ' -f2 | sort -n | tail -1)
BY_SYM=1

echo "const * char $ERROR_VAR[$MAX];"

if [ "$BY_SYM" -eq 1 ]; then
   errno -l | sort -n -k 2 | while read NAME NUM _; do
      echo "$ERROR_VAR[$NAME] = \"$NAME\"; // $NUM"
   done
else
   errno -l | sort -n -k 2 | while read NAME NUM _; do
      echo "$ERROR_VAR[$NUM] = \"$NAME\";"
   done
fi

#errno -l | sed -r 's/([A-Z0-9]+) ([0-9]+).*/\2 \1/g' | sort -n | while read n e
