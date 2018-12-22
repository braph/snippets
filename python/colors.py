#!/usr/bin/python3

BLACK   = "\033[0;30m"
RED     = "\033[0;31m"  
GREEN   = "\033[0;32m"
YELLOW  = "\033[0;33m"
BLUE    = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN    = "\033[0;36m"
WHITE   = "\033[0;37m"

BRIGHT_BLACK   = "\033[1;30m"
BRIGHT_RED     = "\033[1;31m"  
BRIGHT_GREEN   = "\033[1;32m"
BRIGHT_YELLOW  = "\033[1;33m"
BRIGHT_BLUE    = "\033[1;34m"
BRIGHT_MAGENTA = "\033[1;35m"
BRIGHT_CYAN    = "\033[1;36m"
BRIGHT_WHITE   = "\033[1;37m"

RESET   = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

colors = {
    'red':      RED,
    'green':    GREEN,
    'yellow':   YELLOW,
    'blue':     BLUE,
    'magenta':  MAGENTA,
    'cyan':     CYAN,
    'white':    WHITE,
    'black':    BLACK,

    'bright_red':      BRIGHT_RED,
    'bright_green':    BRIGHT_GREEN,
    'bright_yellow':   BRIGHT_YELLOW,
    'bright_blue':     BRIGHT_BLUE,
    'bright_magenta':  BRIGHT_MAGENTA,
    'bright_cyan':     BRIGHT_CYAN,
    'bright_white':    BRIGHT_WHITE,
    'bright_black':    BRIGHT_BLACK,

    'reset':    RESET,
    'bold':     BOLD,
    'reverse':  REVERSE
}

if __name__ == '__main__':
    for name, ansi in colors.items():
        print(ansi, name, RESET)
