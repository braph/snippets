#ifndef _CLASS_H
#define _CLASS_H

/* Seriously, DO NOT USE THIS!!! */

/* Macros for creating "classes"
 *
 * Syntax:
 *
 * #define BASE  <CLASS>
 * #define KLASS <CLASS>
 *
 * __class__(<FIELDS>);
 *
 * <TYPE> __method__(<NAME>, <ARGS>) {
 *    this.field = ...;
 *    self->field = ...;
 * }
 * 
 * #undef KLASS
 *
 * Syntax for usage:
 *  call(void *OBJECT, METHOD, ARGS)
 */

#define METHOD1(klass, __method__)   klass ## _ ## __method__
#define METHOD0(...)                 METHOD1(__VA_ARGS__)
#define __method__(name)             METHOD0(KLASS, name)

#define __class__(...) \
  typedef struct KLASS { __VA_ARGS__ } KLASS

#define return_class_object(...)  \
  KLASS obj = {                   \
    .free = &free,                \
    __VA_ARGS__                   \
  }; return memdup(&obj)

#define destroy(...) \
  void __method__(free) (void *self) { __VA_ARGS__; free(self) }

#define obj_free(OBJECT) \
  OBJECT->free(OBJECT)

#define this \
  (*((KLASS *) self))

#define SELF \
  KLASS* self

#endif
