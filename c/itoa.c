#include <stdio.h>

const char* itoa(int i) {
  #define ITOA_BUFSZ 11
  static char buf[ITOA_BUFSZ] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
  char *b  = &buf[ITOA_BUFSZ];

  do {
    --b;
    *b = (i % 10) + '0';
    i /= 10;
  } while(i);

  return b;
}

int main() {
  printf("%s\n", itoa(0));
  printf("%s\n", itoa(1));
  printf("%s\n", itoa(10));
  printf("%s\n", itoa(9));
  printf("%s\n", itoa(99));
  printf("%s\n", itoa(999));
  printf("%s\n", itoa(1000000001));
}
