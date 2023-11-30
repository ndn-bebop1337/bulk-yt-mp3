#!/usr/bin/python3

"""
Bulk YouTube to MP3
A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos or entire playlists. By default, all downloads are stored in the users home directory. 

Version 1.0
By Brandon REDACTED
"""

import os
import sys
import getopt
from lib import manager
from lib import validator

def main(argv):
    """ Process command line arguments and control
    program work flow

    Arguments:
        argv - list - Provided CLI arguments
    """

    try:
        opts, args = getopt.getopt(argv, "hvVo:s:p:", ["help", "version", "verbosity", "outdir=", "single=", "playlist="])

    except getopt.GetoptError as err_msg:
        print(err_msg)
        exit(0)

    # Set variables with default values
    verbosity = False
    outdir = "{}/".format(os.getenv("HOME"))
    video_urls = []
    playlist_url = None

    # Process options
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\t{} [-h] [-v] [-V] [-o OUTPUT_DIRECTORY] [-s VIDEO_URL] [-p PLAYLIST_URL] VIDEO_URLS".format(sys.argv[0]))
            print("")
            print("A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos or entire playlists. By default, all downloads are stored in the users home directory.")
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
            print("Version 1.0")
            print("By Brandon REDACTED")
            exit(0)

        elif opt in ("-V", "--verbose"):
            # Enable verbosity
            verbosity = True

        elif opt in ("-o", "--outdir"):
            # Specify output directory
            outdir = arg

        elif opt in ("-s", "--single"):
            # Specify video to download
            video_urls.append(arg)

        elif opt in ("-p", "--playlist"):
            # Specify playlist to download 
            playlist_url = arg

        else:
            # Display error message and exit
            print("[E] No such argument: {}".format(opt))
            exit(0)

    # Process arguments
    if len(args) > 0:
        for arg in args:
            video_urls.append(arg)

    # Display banner message
    print("")
    print("#################№#####")
    print("# Bulk YouTube to MP3 #")
    print("# Version 1.0         #")
    print("#######################")
    print("[I] Initializing program...")

    # Create a new instance of the data validator
    data_validator = validator.Validator(verbosity)

    # Sanatize the output directory if it is not the default
    if outdir != "{}/".format(os.getenv("HOME")):
        # Verbose output
        if verbosity == True:
            print("[DEBUGGING] Sanatizing user specified output directory...")

        outdir = data_validator.sanatize_path(outdir)

    # Tell the user where the output directory is
    print("[I] Output directory set to: {}".format(outdir))
    

    # Initialize a new download manager
    download_manager = manager.DownloadManager(verbosity, data_validator)
    
    # Download individual videos
    if len(video_urls) > 0:
        for video_url in video_urls:
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

        # Tell the user how many videos are in the playlist
        print("[I] This playlist has {} videos in it. Beginning download...".format(len(video_list)))

        for row in video_list:
            print("[I] Downloading {0} as {1}...".format(row[0], row[1]))
            download_manager.download_single_video(row[0], row[1])
            print("\t[***] Download successful!")

# Begin execution
if __name__ == "__main__":
    main(sys.argv[1:])
