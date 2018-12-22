#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <utmp.h>
#include <time.h>
#include <getopt.h>

int main(int argc, char *argv[])
{
   int c;

   if (argc < 2)
   {
      printf("missing arg\n");
      return 1;
   }

   struct tm curr_tm;

   memset(&curr_tm, 0, sizeof(struct tm));

   strptime((const char *) argv[3], (const char *) argv[2], &curr_tm);

   //utmpname(argv[1]);
   utmpname(NULL);

   setutent();

   struct utmp *ut_entry = NULL;
   
   while ((ut_entry = getutent()) != NULL)
   {
      printf("ID: %s\n", ut_entry->ut_id);
      printf("Type: %d\n", ut_entry->ut_type);
      printf("User: %s\n", ut_entry->ut_user);
      printf("Host: %s\n", ut_entry->ut_host);
      printf("Time: %d\n", ut_entry->ut_tv.tv_sec);
      printf("\n");

      continue;

      if (ut_entry->ut_type == BOOT_TIME)
      {
         ut_entry->ut_tv.tv_sec = mktime(&curr_tm);
         pututline(ut_entry);
      }
   }

   endutent();
   return 0;
}
