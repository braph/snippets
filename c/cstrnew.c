#define STRING_GET_REFCNT(S) \
  (S + strlen(s) + 2)

#define STRING_GET_REFCNT_WL(S, LEN) \
  (S + LEN + 2)

char* string_dup(char *s) {
  unsigned char* refcnt = STRING_GET_REFCNT(s);
  *refcnt++;
  return s;
}

char* string_from_chars(char *chars) {
  int slen = strlen(chars);
  char *s  = malloc(slen + 2);
  strcpy(s, chars);
  unsigned char* refcnt = STRING_GET_REFCNT_WL(s, slen);
  *refcnt = 1;
  return s;
}

char* string_from_char(char c) {
  char buf[2] = { c, 0 };
  return string_from_chars(buf);
}

void string_free(char *s) {
  unsigned char* refcnt = STRING_GET_REFCNT(s);
  if (--*refcnt)
    free(s);
}
