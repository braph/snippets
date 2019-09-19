// Indent a block of lines
static char* indent(const char *str, int pad) {
  int  ind = -1;
  char res[8192];

  goto INDENT; // First indent does not depend on newline

  do {
    res[++ind] = *str;
    if (*str++ == '\n')
INDENT:
      for (int i = pad; i--;)
        res[++ind] = ' ';
  } while (*str);

  res[++ind] = '\0';
  return strdup(res);
}

