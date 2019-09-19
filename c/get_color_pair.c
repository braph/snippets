
/* Wrapper around ncurses init_pair() that ensures
 * each color pair is only defined once. */
int get_color_pair(short fg, short bg)
{
	static int color_pairs_defined = 0;
	short i, pair_fg, pair_bg;

	for (i = 1; i <= color_pairs_defined; ++i) {
		if (OK == pair_content(i, &pair_fg, &pair_bg))
			if (pair_fg == fg && pair_bg == bg)
				return i;
	}

	if (color_pairs_defined + 1 < COLOR_PAIRS) {
		++color_pairs_defined;
		init_pair(color_pairs_defined, fg, bg);
		return color_pairs_defined;
	}

   return 0;
}

