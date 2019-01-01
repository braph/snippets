#include <string.h>

#define Switch(VAR) \
   {                                         \
      const char *__switch_var = VAR;        \
      if (0) { }                             \

#define Case(STRING) \
      else if (! strcmp(__switch_var, STRING)) {

#define Default \
      else {

#define End \
   }
      
#include <stdio.h>

int main() {
   const char *s1 = "test";
   const char *s2 = "test2";

   Switch(s1)
      Case("test")
         printf("s1 is test\n");

         Switch(s2) 
            Case("test2")  printf("s2 is test2\n");  End
         End

         Switch(s2) 
            Case("asdfsf") printf("error\n");        End
            Default        printf("yeah default\n"); End
         End
      End
      
      Case("asdf")
         printf("s1 is asdf\n");
      End
   End
}
