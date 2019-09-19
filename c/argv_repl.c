
/*
 * instead of an const char *[] = {"A", "B", NULL}
 * use: const char * = "A\0B\0C\0"
 *
 * and this code:
 */

...(const char *_arguments) {
  // make temp array: (untested)
  char *arguments[MAX];
  while (*str) {
    arguments[i++] = str;
    while (*++str != '\0');
    ++str;
  }

  // iterate
  for (const char *str = _arguments; *str; str += (1+strlen(str))) {
  }

  // version if string is not null, but space-delimited (untested)
  char *arguments[MAX];
  char  data[MAX], *d = data;
  strcpy(&data, _arguments);
  while (*d) {
    arguments[i++] = d;
    while (*++d && *d != ' ');
    *d = '\0';
  }
}

// iterate an argv: (without the need of dereferencing $arg)
for (const char **args = argv, *arg = *args; arg; arg = *++args)
for (const char **opts = cmd->opts, *opt = *opts; opt; opt = *++opts)
