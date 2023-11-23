#!/usr/bin/python3

"""
Bulk YouTube to MP3
A simple utility for downloading MP3's from YouTube
videos in bulk. Supports downloading whole playlists or from CSV list of videos.

Version 0.1 Beta
By Brandon REDACTED
"""

import os
import sys
import getopt
from lib import manager

def main(argv):
    """ Process command line arguments and control
    program work flow

    Arguments:
        argv - list - Provided CLI arguments
    """

    try:
        opts, args = getopt.getopt(argv, "hvo:s:p:c:", ["help", "version", "outfile=", "single=", "playlist=", "csv="])

    except getopt.GetoptError as err_msg:
        print(err_msg)
        exit(0)

    # Set variables with default values
    outdir = None
    video_url = None
    playlist_url = None
    csv_file = None

    # Process arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\t{} [-h] [-v] [-o OUTPUT_DIRECTORY] [-s VIDEO_URL] [-p PLAYLIST_URL] [-c CSV_FILE]".format(sys.argv[0]))
            print("")
            print("ARGUMENTS:")
            print("\t-h, --help/tDisplay the help message")
            print("\t-v, --version\tDisplay the version message")
            print("\t-o, --outdir OUTPUT_DIRECTORY\tDirectory to output MP3's to")
            print("\t-s, --single VIDEO_URL\tDownload from single video")
            print("\t-p, --playlist PLAYLIST_URL\tDownload from playlist")
            print("\t-c, --csv CSV_FILE\tDownload from CSV file")
            exit(0)

        elif opt in ("-v", "--version"):
            # Display the version message and exit
            print("Bulk YouTube to MP3")
            print("Version 0.1 Beta")
            print("By Brandon REDACTED")
            exit(0)

        elif opt in ("-o", "--outfile"):
            # Specify output directory
            outdir = arg

        elif opt in ("-s", "--single"):
            # Specify video to download
            video_url = arg

        elif opt in ("-p", "--playlist"):
            # Specify playlist to download 
            playlist_url = arg

        elif opt in ("-c", "--csv"):
            # Specify CSV file to download from
            csv_file = arg

        else:
            # Display error message and exit
            print("[E] No such argument: {}".format(opt))
            exit(0)

    # Display banner message
    print("")
    print("#################№#####")
    print("# Bulk YouTube to MP3 #")
    print("# Version 0.1 Beta    #")
    print("#######################")
    print("[I] Initializing program...")

    # Initialize a new download manager
    download_manager = manager.DownloadManager(outdir
                                               )
    # Download individual videos
    if video_url != None:
        print("[I] Downloading {}...".format(video_url))
        download_manager.download_mp3(video_url, "download.mp3")
        print("\t[***] Download successful!")

    # Download videos from playlist
    if playlist_url != None:
        video_list = download_manager.parse_playlist(playlist_url)

        for row in video_list:
            print("[I] Downloading {0} as {1}...".format(row[0], row[1]))
            download_manager.download_mp3(row[0], row[1])
            print("\t[***] Download successful!")

    # Download videos from CSV file
    if csv_file != None:
        video_list = download_manager.parse_csv(csv_file)

        for row in video_list:
            print("[I] Downloading {0} as {1}".format(row[0], row[1]))
            download_manager.download_mp3(row[0], row[1])
            print("\t[***] Download successful!")

# Begin execution
if __name__ == "__main__":
    main(sys.argv[1:])
