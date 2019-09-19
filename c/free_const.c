
extern char end;

char* strdup_const(const char *s) {
  //debug("%X > %X", s, &end);
  if (s > &end)
    return strdup(s);
  else
    return (char*) s;
}

void free_const(void *ptr) {
  if (ptr > (void*) &end)
    free(ptr);
}
