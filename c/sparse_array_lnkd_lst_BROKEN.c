/*
 * <array_t>
 *  +- <array_head idx=0, len=3>  [0]
 *  |  +- <array_element>         [1]
 *  |     +- <array_element>      [2]
 *  |        +- <array_element>   [3]
 *  |
 *  +- <array_head idx=10, len=3> [10]
 *     +- <array_element>         [11]
 *        +- <array_element>      [12]
 */

typedef char* vstr;
#include <stdlib.h>
#include <assert.h>

#define array_new()           calloc(1, sizeof(array_t))
#define array_head_new()      calloc(1, sizeof(array_head_t))
#define array_element_new()   calloc(1, sizeof(array_element_t))
#define BRK

typedef struct array_element_t {
  vstr val;
  struct array_element_t *next;
} array_element_t;

struct array_head_t;
typedef struct array_head_t {
  vstr val;
  array_element_t *next;
  // -------------------- //
  int  idx;
  int  len;
  struct array_head_t *next_head;
  array_element_t     *last;
} array_head_t;

typedef struct array_t {
  array_head_t *head;
  array_head_t *last_head;
} array_t;

int array_len(array_t *arr) {
  int len = 0;
  if (arr->head)
    for (array_head_t *hed = arr->head; hed; hed = hed->next_head)
      len += hed->len;
  return len;
}

// Function for faster insertion after ``array_append``
array_head_t* array_append_consecutive(array_t *arr, vstr v) {
  array_head_t* head = arr->last_head;
  head->len++;
  array_element_t* new = array_element_new();
  new->val = v;
  //new->next = 0;
  if (head->last) // TODO
    head->last->next = new;
  if (!head->next)
    head->next = new;
  head->last = new;
  return head;
}

array_head_t* array_append(array_t *arr, vstr v) {
  if (! arr->head) {
    // This is a fresh array
    arr->head = array_head_new();
    arr->head->len = 1;
    arr->head->val = v;
    arr->last_head = arr->head;
    //arr->head->idx = 0;
    //arr->head->next = 0;
    //arr->head->last = 0;
    //arr->head->next_head = 0;
    return arr->head;
  }
  else {
    return array_append_consecutive(arr, v);
  }
}

#include <stdio.h>
array_element_t*
array_element_by_index(array_t *arr, array_head_t **in_head, int index) {
  if (!arr->head || index < arr->head->idx ||
      index > arr->last_head->idx + arr->last_head->len)
    return NULL;

  array_element_t *elem;
  array_head_t    *head = arr->head;

  while (head) {
    //printf("head->idx %d == index %d\n", head->idx, index);
    if (index == head->idx) {
      *in_head = head;
      return (array_element_t*) head;
    }
    else if (index < head->idx) {
      //printf("break\n");
      break; // numbers do not get smaller
    }
    else if (index <= head->idx + head->len) {
      elem = head->next;
      for (index = index - head->idx - 1; index--;) {
        //printf("index=%d\n", index);
        assert(elem);
        elem = elem->next;
        assert(elem);
      }
      assert(elem);
      *in_head = head;
      return elem;

    }
    head->next_head;
  }

  return NULL;
}

#ifdef TEST_ARRAY
#include <stdio.h>
int main(int argc, char **argv) {
  int i, j;
  array_t *arr = array_new();
  array_element_t *elem;
  array_head_t *head;

  for (i = 0; i < argc; ++i) {
    printf("%s\n", argv[i]);
    array_append(arr, argv[i]);
    elem = array_element_by_index(arr, &head, i);
    printf("%s\n", elem->val);
  }

  return;

  for (j = 0; j < argc; ++j) {
    i = j + 400;
    printf("%s\n", argv[i]);
    array_append(arr, argv[i]);
    elem = array_element_by_index(arr, &head, i);
    printf("%s\n", elem->val);
  }

}
#endif
