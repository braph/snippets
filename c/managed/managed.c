#include "managed.h"

typedef struct managed_pointer_t {
  managed_ptr_t ptr;
  int refcount;
} managed_pointer_t;

static managed_pointer_t *pointers;
static int pointers_size;

managed_ptr_t managed_ptr_ref(managed_ptr_t ptr) {
  int i = -1;
  int i_free_slot = -1;

  while (++i < pointers_size) {
    if (pointers[i].ptr == ptr) {
      ++pointers[i].refcount;
      goto RETURN;
    }
    else if (i_free_slot == -1 && pointers[i].ptr == NULL) {
      i_free_slot = i;
    }
  }

  if (i_free_slot != -1) {
    pointers[i_free_slot].ptr = ptr;
    pointers[i_free_slot].refcount = 1;
    goto RETURN;
  }

  pointers_size += 16;
  pointers = realloc(pointers, pointers_size * sizeof(managed_pointer_t));

  pointers[i].ptr = ptr;
  pointers[i].refcount = 1;

  // TODO: memset()
  while (++i < pointers_size) {
    pointers[i].ptr = NULL;
  }

RETURN:
  return ptr;
}

int managed_ptr_unref(managed_ptr_t ptr) {
  for (int i = -1; ++i < pointers_size;) {
    if (pointers[i].ptr == ptr) {
      if (--(pointers[i].refcount) <= 0) {
        pointers[i].ptr = NULL;
        return 1;
      }
      else
        return 0;
    }
  }

  return 1; // ptr not found -> not managed by us -> can free
}
