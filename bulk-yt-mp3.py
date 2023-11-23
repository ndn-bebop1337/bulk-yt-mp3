#!/usr/bin/python3

"""
Bulk YouTube to MP3
A simple utility for downloading MP3's from YouTube
videos in bulk. Can download either individual videos or whole playlists

Version 0.2 Beta
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
        opts, args = getopt.getopt(argv, "hvVo:s:p:", ["help", "version", "verbosity", "outfile=", "single=", "playlist="])

    except getopt.GetoptError as err_msg:
        print(err_msg)
        exit(0)

    # Set variables with default values
    verbosity = False
    outdir = "{}/".format(os.getenv("HOME"))
    video_url = None
    playlist_url = None

    # Process arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\t{} [-h] [-v] [-V] [-o OUTPUT_DIRECTORY] [-s VIDEO_URL] [-p PLAYLIST_URL]".format(sys.argv[0]))
            print("")
            print("ARGUMENTS:")
            print("\t-h, --help/tDisplay the help message")
            print("\t-v, --version\tDisplay the version message")
            print("\t-V, --verbose\tEnable verbosity")
            print("\t-o, --outdir OUTPUT_DIRECTORY\tDirectory to output MP3's to")
            print("\t-s, --single VIDEO_URL\tDownload from single video")
            print("\t-p, --playlist PLAYLIST_URL\tDownload from playlist")
            exit(0)

        elif opt in ("-v", "--version"):
            # Display the version message and exit
            print("Bulk YouTube to MP3")
            print("Version 0.2 Beta")
            print("By Brandon REDACTED")
            exit(0)

        elif opt in ("-V", "--verbose"):
            # Enable verbosity
            verbosity = True

        elif opt in ("-o", "--outfile"):
            # Specify output directory
            outdir = arg

        elif opt in ("-s", "--single"):
            # Specify video to download
            video_url = arg

        elif opt in ("-p", "--playlist"):
            # Specify playlist to download 
            playlist_url = arg

        else:
            # Display error message and exit
            print("[E] No such argument: {}".format(opt))
            exit(0)

    # Display banner message
    print("")
    print("#################№#####")
    print("# Bulk YouTube to MP3 #")
    print("# Version 0.2 Beta    #")
    print("#######################")
    print("[I] Initializing program...")

    # Initialize a new download manager
    download_manager = manager.DownloadManager(verbosity)
    
    # Download individual videos
    if video_url != None:
        # Get the video title
        video_title = download_manager.get_video_title(video_url)

        # Specify the download location
        download_manager.change_output_directory(outdir)

        # Download the video
        print("[I] Downloading {}...".format(video_url))
        download_manager.download_single_video(video_url, "{}.mp3".format(video_title))
        print("\t[***] Download successful!")

    # Download videos from playlist
    if playlist_url != None:
        # Get the playlist title
        playlist_title = download_manager.get_playlist_title(playlist_url)

        # Create the directory to download to and specify it as the new download location
        playlist_download_directory = os.path.join(outdir, "{}/".format(playlist_title))
        os.mkdir(playlist_download_directory)
        download_manager.change_output_directory(playlist_download_directory)
        
        # Parse the playlist
        video_list = download_manager.parse_playlist(playlist_url)

        for row in video_list:
            print("[I] Downloading {0} as {1}...".format(row[0], row[1]))
            download_manager.download_single_video(row[0], row[1])
            print("\t[***] Download successful!")

# Begin execution
if __name__ == "__main__":
    main(sys.argv[1:])
