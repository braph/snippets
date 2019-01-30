ssize_t _send(int sockfd, const void *buf, size_t len, int flags) {
   ssize_t r;
   for (int i = 0; i < 10; ++i) {
      if ((r = send(sockfd, buf, len, flags)) < 0)
         if (errno == EAGAIN) {
            sleep(1); continue;
         }
      return r;
   }
   return r;
}
