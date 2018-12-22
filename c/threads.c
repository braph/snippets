
pthread_t *threads = NULL;
size_t num_threads = 0;

void add_thread(pthread_t thread) {
   for (int i = 0; i < num_threads; ++i) {
      if (threads[i] == 0) {
         threads[i] = thread;
         return;
      }
   }

   threads = realloc(threads, ++num_threads * sizeof(pthread_t));
   threads[num_threads - 1] = thread;
}

void remove_thread(pthread_t thread) {
   for (int i = 0; i < num_threads; ++i) {
      if (threads[i] != 0 && pthread_equal(threads[i], thread)) {
         threads[i] = 0;
         return;
      }
   }
}

