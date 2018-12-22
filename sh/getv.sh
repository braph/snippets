#!/bin/bash

DEBUG=0
DEBUG_LOG=/dev/shm/p.debug.log

urldecode()
{
   perl -MURI::Escape=uri_unescape -ne 'print uri_unescape($_)'
}

get_source_default()
{
   echo "get_source_default('$1')" >&2
   local src;
   #src=$( wget -qO- "$1" )
   src=$( curl -L "$1" )

   (( DEBUG )) && printf "$0:\n%s" "$src" >> "$DEBUG_LOG"

   echo "$src"
}

get_source_youporn()
{
   curl --cookie "age_verified=1" "$1";
}

get_source_tnaflix()
{
   echo "get_source_tnaflix()" >&2
   wget -qO- -U Firefox "$1"
}

grep_video_default()
{
   grep -Eio "//[^'\"]+\.(m4v|mp4|flv|mkv|avi)(/|([^|<>\"'\.][^<>'\"]+))?" | sed "s!^//!http://!g"
}

grep_fid_videos()
{
   local fid;
   grep -Eio "//[^'\"]+\.(fid)([^<>\"'\.][^<>'\"]+)?" | sed "s!^//!http://!g" | sort | uniq | while read -r fid; do
      get_source_default "$fid"
   done
}

drop_images()
{
   grep -v -i -E '\.(jpe?g|png|gif)$';
}

strstr()
{
   grep -qF "$1" <<< "$2";
}

get_domain()
{
   sed 's!^.*://!!; s!/.*!!g' <<< "$1";
}

get_video_streams()
{
   echo "$0: Processing $1" >&2

   local src;

   if
      strstr "pornodue.com" "$1" ||
      strstr "pornhub.com" "$1"
   then
      echo "not supported" >&2
      return
   fi

   if strstr "youporn.com" "$1"; then
      src=$(get_source_youporn "$1") || return;

   elif strstr "perfectgirls.net" "$1"; then
      src=$(get_source_tnaflix "$1") || return;

      new_url=$( grep -Eo '/get/[0-9]+\.mp4' <<< "$src" )
      new_url="http://www.perfectgirls.net$new_url";

      src=$(get_source_tnaflix "$new_url");
      #get_video_streams "$new_url"; return;

   elif strstr 'tnaflix.com' "$1" || strstr drtuber "$1"; then
      src=$(get_source_tnaflix "$1") || return;

   elif strstr 'youtube.com' "$1"; then
      videos=$(youtube-dl -g "$1");
      while read -r video; do
         play "$video"
      done <<< "$videos"
      return;

   elif strstr 'eporner.com' "$1"; then
      src=$(get_source_tnaflix "$1") || return;

      src=$(grep -Eo "/dload[^\"]+" <<< "$src" | sed s,^,http://www.eporner.com,g)

#src=$(
#      while read -r x; do
#         curl -D- "$x"
#      done <<< "$src"
#      )

   else
      src=$(get_source_default "$1") || return;
   fi;

   if strstr 'spankwire' "$1" || strstr xvideos "$1" || strstr 'xnxx.com' "$1"; then
      src=$(urldecode <<< "$src");
      src=$(sed 's/&amp;/\n/g' <<< "$src")
#src=$(grep_fid_videos <<< "$src");

   elif strstr 'empflix.com' "$1"; then
      src=$(grep_fid_videos <<< "$src");

   elif strstr 'keezmovies.com' "$1"; then
      src=${src//\\\//\/};
   fi

   videos=$(grep_video_default <<< "$src");
   videos=$(drop_images <<< "$videos" | sort | uniq);

   play_videos;
}

play_videos()
{
   local video;
   while read -r video; do
      grep -q -- "-$" <<< "$video" && continue
      play "$video"
   done <<< "$videos"
}

play()
{
   echo "$1"
   mpv "$1"
#mpv --no-cache --mute=yes --no-ytdl "$1";
}

for arg; do
   echo "$0: processing $arg" >&2

   if grep -q -F .flv <<< "$arg"; then
      play "$arg"
   else
      get_video_streams "$arg"
   fi
done
