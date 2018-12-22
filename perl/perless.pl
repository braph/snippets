#!/usr/bin/perl

# example program for dealing with curses

use strict;
use warnings;
use autodie;

use Curses;


open(my $fh, "<", $ARGV[0]);
my @file = <$fh>;
close $fh;


my $curses = new Curses;
#init_pair(1,2,3);

# generate new window...
my $window = newpad($#file + 1, $COLS);

# add lines
$window->addstr($_, 0, $file[$_]) for (0..$#file);

my $pointer = 0;

clear;
$window->prefresh($pointer, 0, 0, 0, $LINES - 1, $COLS - 1);

while (my $char = $window->getch)
{
   if ($char eq "j" and $pointer < $#file+1 - $LINES)
   {
      $pointer++;
   }
   elsif ($char eq "k" and $pointer > 0)
   {
      $pointer--;
   }
	elsif ($char eq 'g')
	{
		$pointer = 0;
	}
	elsif ($char eq 'G')
	{
		$pointer = $#file+1 - $COLS;
	}
   elsif ($char eq "q")
   {
      endwin;
      exit(0);
   }

	refresh;
	$window->prefresh($pointer, 0, 0, 0, $LINES - 1, $COLS - 1);
}
