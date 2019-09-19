static int strarray_index(const char **haystack, int size, const char *needle) {
	int start = 0;
	int end = size;
	int i, cmp;

	while (1) {
		i = (start+end) / 2;
		cmp = strcmp(needle, haystack[i]);

		if (cmp == 0)
			return i;
		else if (end == start + 1)
			return -1;
		else if (cmp > 0)
			start = i;
		else
			end = i;
	}
}

