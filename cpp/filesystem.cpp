// dropped in favor to boost
#define DEFAULT_PERMS (S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)

  static inline void mkdir(const std::string& dir, mode_t mode = DEFAULT_PERMS) {
    if (::mkdir(dir.c_str(), mode)) {
      const char *msg = std::strerror(errno);
      throw std::invalid_argument(msg);
    }
  }

  static inline void mkdir_p(const std::string& dir, mode_t mode = DEFAULT_PERMS) {
    size_t idx = 0;
    std::string part;

    for (;;) {
      idx = dir.find(PATH_SEP, idx);
      if (idx == std::string::npos)
        break;

      part = dir.substr(0, idx);
      if (part != "")
        std::cout << part << std::endl;
      ++idx;
    }

    if (part != dir)
      std::cout << dir << std::endl;
  }

