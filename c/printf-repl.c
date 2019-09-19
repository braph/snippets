#include <stdarg.h>
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

int snprintf_repl(char *out, size_t size, const char *fmt, ...) {
  if (--size == -1) // Reserve space for '\0'
    return 0;

  int   d;
  char  c;
  const char *s;
  int   slen;
  va_list ap;
  va_start(ap, fmt);

  do {
    if (*fmt == '%') {
      #define case break;case
      switch (*++fmt) {
        case 's':
          s = (char*) va_arg(ap, char*);
          slen = strlen(s);
          if (slen > size)
            return -1;
          strcpy(out, s);
          out += slen;
          size -= slen;
        case 'c':
          c = (char) va_arg(ap, int);
          *out++ = c;
          --size;
        case 'd':
          d = (int) va_arg(ap, int);
          s = itoa(d);
          slen = strlen(s);
          if (slen > size)
            return -1;
          strcpy(out, s);
          out += slen;
          size -= slen;
        case '%':
          *out++ = '%';
      }
      #undef case
    }
    else {
      *out++ = *fmt;
      --size;
    }
  } while(*fmt++);

  va_end(ap);
  return 1;
}

int printf_repl(const char *fmt, ...) {
  int   d;
  char  c;
  const char *s;
  va_list ap;
  va_start(ap, fmt);

  do {
    if (*fmt == '%') {
      #define case break;case
      switch (*++fmt) {
        case 's':
          s = (char*) va_arg(ap, char*);
          write_full(STDOUT_FILENO, s, strlen(s));
        case 'c':
          c = (char) va_arg(ap, int);
          write_full(STDOUT_FILENO, &c, 1);
        case 'd':
          d = (int) va_arg(ap, int);
          s = itoa(d);
          write_full(STDOUT_FILENO, s, strlen(s));
        case '%':
          write_full(STDOUT_FILENO, (const char*) &"s", 1);
      }
      #undef case
    }
    else {
      write_full(STDOUT_FILENO, fmt, 1);
    }
  } while(*fmt++);

  va_end(ap);
  return 1;
}
