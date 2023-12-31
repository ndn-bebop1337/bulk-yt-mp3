#!/usr/bin/python3

"""
gen_csv_from_playlist.py

A helper script that partially automates the creation of tag data CSV files based on YouTube playlists. It's designed mainly for use with music albums, and I originally wrote it to fit my own specific needs so it isn't universal or well documented by any means, but I felt I should include it anyway. 
"""

import os
import sys
import urllib.request
from pytube import YouTube, Playlist

def main(argv):
  # Help message (Groan inducingly added by Bebop just for YOU :D)
  if argv in ("-h", "--help"):
    print("USAGE gen_csv_from_playlist.py PLAYLIST_URL")
    exit(0)

  # List of dicts
  tag_data = []

  playlist = Playlist(argv)
  video_urls = playlist.video_urls

  for url in video_urls:
    video = YouTube(url)
    title = video.title

  

  q = input("[?] Add thumbnail? (1) From YouTube (2) From local image (N) No thumbnail")
  if q == 1:
    # Get thumbnail from YouTube
    img_url = YouTube(video_urls[0]).thumbnail_url
    img_name = "{}_thumbnail.jpg".format(playlist.title)
    urllib.request.urlretrieve(img_url, img_name)
    thumbnail_file = img_name

  elif q == 2:
    # Get thumbnail from local file
    thumbnail_file = input("[?] Path to thumbnail: ")

  elif q in ("n" or "N"):
    # No thumbnail


# Run the script
if __name__ == "__main__":
  main(sys.argv[1]\\\\\\\\