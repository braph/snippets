#include <err.h>
#include <stdio.h>
#include <stdlib.h>

// 4932;

void dmp_arr(int *values) {
  while (*values) {
    printf("%d ", *values);
    ++values;
  }
}

int in_arr(int value, int *values) {
  while (*values) {
    if (value == *values) {
      return 1;
    }
    else
      ++values;
  }

  return 0;
}

void print_i(int i) {
  if (i % 10)
    printf("%d", i % 10);
  else
    printf(" %d ", (i / 10) * 10);
}

int cp(const char *src, const char *dest, int *skip) {
  FILE *src_fh, *dest_fh;
  char buf[1024];
  int nread;
  int i = 0;

  if (! (src_fh = fopen(src, "r"))) {
    perror(src);
    return 0;
  }

  if (! (dest_fh = fopen(dest, "w"))) {
    perror(dest);
    return 0;
  }

  setbuf(src_fh, NULL);

  while (++i) {
    if (in_arr(i, skip)) {
      printf("\nskipping %d\n", i);
      fseek(src_fh, 1024, SEEK_CUR);
      continue;
    }

    nread = fread(buf, 1, sizeof(buf), src_fh);

    //printf("%d ", i);
    print_i(i);

    if (! nread) {
      perror("Read");
      break;
    }

    fwrite(buf, 1, nread, dest_fh);
  }
}

int main(int argc, char **argv)
{
  int argi;
  int skip[8192];
  int skip_i = 0;

  if (argc < 2)
    err(1, "argc < 2");

  for (int argi = 2; ++argi < argc;) {

    int from, to;
    if (2 == sscanf(argv[argi], "%d-%d", &from, &to)) {
      for (; from <= to; ++from)
        skip[skip_i++] = from;
    }
    else {
      skip[skip_i++] = atoi(argv[argi]);
    }
  }
  skip[skip_i] = 0;

  //dmp_arr(skip); return 0;

  cp(argv[1], argv[2], skip);
  return 0;
}

