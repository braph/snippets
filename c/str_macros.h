// === strpaste macros ========================================================
#define strpaste2(DEST, SRC1, SRC2) \
  strcat(strcpy(DEST, SRC1), SRC2)

#define strpaste3(DEST, SRC1, SRC2, SRC3) \
  strcat(strcat(strcpy(DEST, SRC1), SRC2), SRC3)

#define strpaste4(DEST, SRC1, SRC2, SRC3, SRC4) \
  strcat(strcat(strcat(strcpy(DEST, SRC1), SRC2), SRC3), SRC4)

// === strlen macros ==========================================================
#define strlen2(S1, S2) \
  strlen(S1) + strlen(S2)

#define strlen3(S1, S2, S3) \
  strlen(S1) + strlen(S2) + strlen(S3)

#define strlen4(S1, S2, S3, S4) \
  strlen(S1) + strlen(S2) + strlen(S3) + strlen(S4)

