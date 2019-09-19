struct strings_t {
  int refcnt;
  int size;
  string_t strings[1];
}

strings_t* strings_dup(strings_t *s) {
  for (int i = 0; i < s.size; ++i)
    string_dup(s.strings[i]);
  s.refcnt++;
  return s;
}

struct string_t {
  int  refcnt;
  int  size;
  char str[1];
};

string_t* string_dup(string_t *s) {
  s->refcnt++;
  return s;
}

string_t* string_from_char(char c) {
  string_t *s = malloc(sizeof(string_t) + 1);
  s->refcnt = 1;
  s->size   = 1;
  s->str[0] = c;
  s->str[1] = 0;
}

string_t* string_from_chars(char *chars) {
  int slen    = strlen(chars);
  string_t *s = malloc(sizeof(string_t) + slen);
  s->refcnt   = 1;
  s->size     = slen;
  strcpy(s->string, chars);
}

string_t* string_free(string_t *s) {
  if (--s->refcnt)
    free(s);
}
