#ifndef _MANAGED_H
#define _MANAGED_H

#include <stdlib.h>

/* Managed pointers. */

#define PTR_REF(...) \
  managed_ptr_ref(__VA_ARGS__)

#define PTR_UNREF(...) \
  managed_ptr_unref(__VA_ARGS__)

typedef void* managed_ptr_t;

managed_ptr_t managed_ptr_ref(managed_ptr_t ptr);
int           managed_ptr_unref(managed_ptr_t ptr);

#endif
