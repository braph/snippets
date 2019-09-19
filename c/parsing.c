static unsigned int read_hex() {
  int c;
  unsigned int val = 0;

  while (isxdigit((c = lex_getc())))
    val = val * 16 + 
      (c <= '9' ? c - '0'      :
      (c <= 'F' ? c - 'A' + 10 :
       c - 'a' + 10));
  lex_unget();
  return val;
}

static unsigned int read_oct() {
  int c;
  unsigned int val = 0;

  while ((c = lex_getc()) >= '0' && c < '8')
    val = val * 8 + c - '0';
  lex_unget();
  return val;
}

static unsigned int read_dec() {
  int c;
  unsigned val = 0;

  while (isdigit((c = lex_getc())))
    val = val * 10 + c - '0';
  lex_unget();
  return val;
}

