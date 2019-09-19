#include "options.h"
#include "errormsg.h"

#include <string.h>
#include <stdlib.h>

/*
 * Parse options, return the index of first non option or -1 on failure
 */
int parse_options(int argc, char *args[], const char *optstr, option **opts) {
  *opts = NULL;

  int c;
  opterr = 0;
  while ((c = getopt(argc, args, optstr)) != -1) {
    switch (c) {
      case '?':
        error_setf(
            (strchr(optstr, optopt) ? E_MISSING_ARG : E_UNKNOWN_OPT),
            "-%c", optopt);
        goto ERROR;

      default:
        *opts = realloc(*opts, (2 + ++opti) * sizeof(option));
        (*opts)[opti].opt = *c;

        if (*(strchr(optstr, c) + 1) == ':')
          (*opts)[opti].arg = optarg;
    }
  }

RETURN:
  if (opti == -1)
    *opts = calloc(1, sizeof(option));
  else
    (*opts)[++opti].opt = 0;
  return i;

ERROR:
  free(*opts);
  return -1;
}

/*
 * Parse options, modify argc and argv, return 1 on success, 0 on failure
 */
int get_options(int *argc, char **args[], const char *optstr, option **opts) {
  int optind = parse_options(*argc, *args, optstr, opts);
  if (optind == -1)
    return 0;

  *argc -= optind;
  *args  = &(*args)[optind];
  return 1;
}
