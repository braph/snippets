
NOT_WORKING:

// === Replacing those saves us some bytes ====================================
#include <stropts.h>
#include <termios.h>
#include <term.h>
#define tcgetattr(FD, ARG) \
  ioctl(FD, TCGETA, ARG)

#define tcsetattr(FD, CMD, ARG) \
  ioctl(FD, CMD, ARG)

