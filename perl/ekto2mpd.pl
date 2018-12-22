#!/usr/bin/perl

use strict;
use warnings;
use feature "say";

use Date::Parse;
use Data::Dumper;
use WWW::Mechanize;
use HTML::TokeParser;
use HTML::Entities;
use MIME::Base64;
use Curses;
use Storable;

sub newEktoUrl
{
   return
   {
      "url" => shift,
      "artist" => shift,
      "title" => shift,
      "album" => shift,
      "trackno" => shift,
      "bpm" => shift,
      "date" => shift,
      "style" => shift
   }
}

sub parseAlbum
{
   my ($tokeParser) = (@_);

   my %generalInfo = ( "artist" => '', "album" => '', "date" => '', "style" => '' );
   my @albumSongs = ( newEktoUrl() );

   while (my $tag = $tokeParser->get_tag("a", "span", "script"))
   {
      my ($name, $attr) = ($tag->[0], $tag->[1]);

      # a new album starts with this tag
      if ($name eq "a" and defined $attr->{'rel'} and $attr->{'rel'} eq "bookmark")
      {
         my $value = decode_entities($tokeParser->get_trimmed_text('/a'));

         my $delimiter = decode_entities("&#8211;");

         if ($value =~ /([^&]+) $delimiter (.*)/)
         {
            ($generalInfo{'artist'}, $generalInfo{'album'}) = ($1, $2);
         }
         else
         {
            $generalInfo{'album'} = $value;
         }
      }

      # reading and filling songs
      elsif ($name eq "span" and defined $attr->{'class'})
      {
         my $class = $attr->{'class'};
         my $text = decode_entities($tokeParser->get_trimmed_text("/span"));

         # artist of track
         if ($class eq 'a')
         {
            $albumSongs[-1]->{'artist'} = $text;
         }
         elsif ($class eq 'n')
         {
            $albumSongs[-1]->{'trackno'} = $text;
         }
         elsif ($class eq 'r')
         {
            $albumSongs[-1]->{'title'} .= " " . $text;
         }
         elsif ($class eq 't')
         {
            $albumSongs[-1]->{'title'} = $text;
         }
         elsif ($class eq "style")
         {
            $generalInfo{'style'} = $text;
         }
         elsif ($class eq 'd')
         {
            if ($text =~ m/BPM/)
            {
               $text =~ tr/0-9,.//cd;
               $albumSongs[-1]->{'bpm'} = $text;

               push @albumSongs, newEktoUrl();
            }
            else
            {
               $generalInfo{'date'} = $text;
            }
         }
      }

      # last thing we do
      elsif ($name eq "script")
      {
         my $script = $tokeParser->get_trimmed_text("/script");

         if ($script =~ /soundFile:"([^"]+)/)
         {
            my @urls = split(',', decode_base64($1));

            for my $i (0 .. $#urls)
            {
               $albumSongs[$i]->{'url'} = $urls[$i];

               # fill up some other data
               $albumSongs[$i]{'date'} = $generalInfo{'date'};
               $albumSongs[$i]{'style'} = $generalInfo{'style'};
               $albumSongs[$i]{'album'} = $generalInfo{'album'};

               if (! defined($albumSongs[$i]{'artist'}))
               {
                  $albumSongs[$i]{'artist'} = $generalInfo{'artist'};
               }
            }

            delete @albumSongs[-1];
            return @albumSongs;
         }
      }
   }

   return ();
}

sub parsePage
{
   my ($page) = (@_);

   my $tokeParser = HTML::TokeParser->new($page);
   my @songs = ();

   while (my @album = parseAlbum($tokeParser))
   {
      push @songs, @album;
   }

   return \@songs;
}

package browserWindow;

use Curses;
use Data::Dumper;

sub new
{
   my ($class) = @_;

   my $self = {};

   $self->{"_curses"} = new Curses;

   $self->{"_lastPointer"} = 0;
   $self->{"_numberSongs"} = 0;
   $self->{"_lastSong"} = 0;
   $self->{"_currentPointer"} = 0;
   $self->{"_playlist"} = 0;

   # Format is: [color](length(%)){tag}
   $self->{"_playlistFormat"} = "[blue,left](30%){artist} [yellow](30%){album} [green](30%){track}";

   bless $self, $class;

   $self->parseFormat();

   return $self;
}

sub parseFormat
{
   my ($self) = @_;

   my %colWidths = ();
   my $maxWidth = 80;

   while ($self->{"_playlistFormat"} =~ /(\[\w*\])?(\(\d*%?\))(\{\w*\})\s*/g)
   {
#print "[]=$1\n";
#      print "()=$2\n";
#      print "{}=$3\n";
   }
}

sub printPlaylist
{
   my ($self) = @_;

   $self->{"_curses"}->clear;

   print STDERR "PRINTING PLAYLIST";
   print STDERR Dumper($self->{"_playlist"});

   foreach my $track ($self->{"_playlist"})
   {
      print STDERR "TRACK\n";
      print STDERR Dumper($track);

      foreach my $tag ($track)
      {
         $self->{"_curses"}->addstr($tag . " ");
      }

      $self->{"_curses"}->addstr("\n");
   }

   $self->{"_curses"}->refresh;
}

sub setPos
{
   my ($self, $pos) = @_;

   $self->{'_currentPointer'} = $pos;
}

sub getPos
{
   return $_[0]->{"_currentPointer"};
}

sub draw
{
   my ($self) = @_;

   $self->printPlaylist();
}

sub setPlaylist
{
   my ($self, $playlist) = @_;

   $self->{"_numberSongs"} = scalar $playlist;

   $self->{"_playlist"} = $playlist;

   print STDERR "SETTING PLAYLIST";
   print STDERR Dumper($self->{"_playlist"});

   $self->setPos(0);
}

1;

use Storable;

my $dbfile = "/tmp/db";
my $albums;

eval {
   $albums = retrieve($dbfile);
};

if (! defined($albums))
{
   our $browseUrl = "https://www.ektoplazm.com/section/free-music/page/";
   my $mech = WWW::Mechanize->new();
   $mech->get($browseUrl . '2');

   my $page = \$mech->content();

   $albums = parsePage($page);

   store \$albums, $dbfile;
}

my %windows = (
   "browser" => new browserWindow,
   "help" => new Curses
);

$windows{"browser"}->setPlaylist($albums);
$windows{"browser"}->draw();
