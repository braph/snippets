
int strchr_count(const char *string, char c) {
   int count = 0;
   for (const char *s = strchr(string, c); s; s = strchr(s + 1, c))
      ++count;
   return count;
}
