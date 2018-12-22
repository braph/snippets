
size_t split_command_list(const char *line, char ***list) {
   // command_list_end
   int i;
   size_t size = 0;
   *list = NULL;

   while (*line) {
      i = 0;
      while (*(line + i++) != '\n');
      *list = realloc(*list, ++size * sizeof(char**));
      (*list)[size - 1] = strndup(line, i - 1);
      line += i;
   }

   return size;
}

