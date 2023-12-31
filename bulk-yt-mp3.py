#!/usr/bin/python3

"""
Bulk YouTube to MP3
A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos or entire playlists. By default, all downloads are stored in the users home directory. 

Version 1.5 (Sleep Deprived)
By Brandon REDACTED
"""

import os
import sys
import time
import getopt
import threading
from lib import manager
from lib import tag_editor

def process_queued_videos(verbosity, use_threading, download_manager, video_queue):
    """ Download all queued videos and create threads if enabled

    Arguments:
        verbosity - bool - Verbose output
        use_threading - bool - Use multithreading
        download_manager - Manager object - Download management tool
        video_queue - list of tuples - A list of video url/title/filename tuples
    """
    # Initialize the tag editor
    editor = tag_editor.Editor(verbosity)

    # Initialize the downloader
    downloader = manager.Downloader(download_manager, editor)
    
    """
    Logic for downloading queued videos with multithreading
    """
    # If multithreading is enabled
    if use_threading == True:
        # Initialize a list of all threads
        thread_list = []

        # Output message
        print("[I] Generating download threads...")
        
        # Create a new thread for each video and add it to the list
        for video in video_queue:
            new_thread = threading.Thread(target=downloader.download_and_convert, args=(video[0], video[1], video[2], video[3]))
            thread_list.append(new_thread) 

            # Output message
            print("\t[i] Created thread for video: {}".format(video[0]))

        # Start all the threads, then wait for them to finish
        print("[I] Starting threads, downloads now in progress...")
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        # Output message
        print("[I] Downloads complete. Adding tags...")

    else:
        # Download normally
        print("[I] Downloads now in progress...")
        for video in video_queue:
            print("\t[i] Downloading {0} ({1})".format(video[1], video[0]))
            downloader.download_and_convert(video[0], video[1], video[2], video[3])
        
def main(argv):
    """ Process command line arguments and control
    program work flow

    Arguments:
        argv - list - Provided CLI arguments
    """

    try:
        opts, args = getopt.getopt(argv, "hvVmo:s:p:t:", ["help", "version", "verbosity", "multithreading", "outdir=", "single=", "playlist=", "tags="])

    except getopt.GetoptError as err_msg:
        print(err_msg)
        exit(0)

    # Set variables with default values
    verbosity = False
    use_threading = False
    outdir = os.getcwd()
    video_urls = []
    playlist_url = None
    tag_data_file = None

    # Process options
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\t{} [-h] [-v] [-V] [-m] [-o OUTPUT_DIRECTORY] [-s VIDEO_URL] [-p PLAYLIST_URL] [-t TAG_INFO] VIDEO_URLS".format(sys.argv[0]))
            print("")
            print("A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos or entire playlists. By default, all downloads are stored in the users home directory.")
            print("")
            print("ARGUMENTS:")
            print("\t-h, --help/tDisplay the help message")
            print("\t-v, --version\tDisplay the version message")
            print("\t-V, --verbose\tEnable verbosity")
            print("\t-m, --multithreading\tEnable multithreading")
            print("\t-o, --outdir OUTPUT_DIRECTORY\tDirectory to output MP3's to")
            print("\t-s, --single VIDEO_URL\tDownload from single video")
            print("\t-p, --playlist PLAYLIST_URL\tDownload from playlist")
            print("\t-t, --tags TAG_INFO\tAdd tags to MP3's. Tag info is passed as a list of tuples, see README for more info.")
            exit(0)

        elif opt in ("-v", "--version"):
            # Display the version message and exit
            print("Bulk YouTube to MP3")
            print("Version 1.5 (Sleep Deprived)")
            print("By Brandon REDACTED")
            exit(0)

        elif opt in ("-V", "--verbose"):
            # Enable verbosity
            verbosity = True

        elif opt in ("-m", "--multithreading"):
            # Enable threading
            use_threading = True

        elif opt in ("-o", "--outdir"):
            # Specify output directory
            outdir = arg

        elif opt in ("-s", "--single"):
            # Specify video to download
            video_urls.append(arg)

        elif opt in ("-p", "--playlist"):
            # Specify playlist to download 
            playlist_url = arg

        elif opt in ("-t", "--tags"):
            # Add tags to MP3's
            tag_data_file = arg

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
    print("################################")
    print("# Bulk YouTube to MP3          #")
    print("# Version 1.5 (Sleep Deprived) #")
    print("################################")
    print("[I] Initializing program...")
    
    # Initialize a new download manager
    download_manager = manager.DownloadManager(verbosity)

    # Move script execution to the designated output directory, if applicable
    if outdir != os.getcwd():
        os.chdir(outdir)

    # If a tag data file is present, parse it for inclusion in the video queue
    if tag_data_file != None:
        parsed_tag_data = download_manager.parse_tag_data_file(tag_data_file)

    """
    All videos to be downloaded must be added to the queue, which is a list of tuples containing the video's URL, its title, the desired filename for the end download, and a variable containing either Nonetype or tag data, if it was provided. If the video is to be downloaded into a subdirectory inside of the main output directory, say in the case of an album playlist, said subdirectory must be appended to the beginning of the filename. 
    """
    
    # Initialize queue
    video_queue = []

    """
    Logic for handling and queueing individual videos, specified with either the -s/--single option, or passed as a program argument. This essentially fetches the title associated with each YouTube video URL, builds a filename based off of it and the output directory, and adds all of this data to the download queue
    """
    
    # Handle individual videos
    if len(video_urls) > 0:
        # Output message
        print("[I] Adding video(s) to queue...")

        c = 0
        for video_url in video_urls:
            # If tag data was provided, prepare it for adding to the videos tuple
            if tag_data_file != None:
                video_metadata = parsed_tag_data[c]
            else:
                # If not, create a variable to act as a placeholder
                video_metadata = None
                
            # Get the video title
            video_title = download_manager.get_video_title(video_url)

            # Build the filename and queue video
            video_filename = os.path.join(outdir, "{}.mp3".format(video_title))
            current_vid = (video_url, video_title, video_filename, video_metadata)
            video_queue.append(current_vid)

            # Output m uessage
            print("\t[i] \"{0}\" added to queue.".format(video_title))

            c += 1

    """
    Logic for building the queue from playlists specified with -p/--playlist. It retrieves the playlists title and creates a subdirectory with it, parses the playlist to retrieve the URL and title of all its videos, then gives each video a filename derived from the subdirectory name and the video's title before adding to the queue
    """
    # Parse playlists and add their videos to the queue
    if playlist_url != None:
        # Get the playlist title
        playlist_title = download_manager.get_playlist_title(playlist_url)

        # Create the directory to download to and append it to the filepath of the videos
        playlist_download_directory = os.path.join(outdir, "{}".format(playlist_title))
        os.mkdir(playlist_download_directory)

        # Display the name of the playlist
        print("[I] Name of playlist: {}".format(playlist_title))
        
        # Parse the playlist and add the videos to the queue
        parsed_video_list = download_manager.parse_playlist(playlist_url)

        # Tell the user how many videos are in the playlist and where the outdir is
        print("[I] Number of videos in playlist: {}".format(len(parsed_video_list)))
        print("[I] Download location for playlist videos: {}".format(playlist_download_directory))
        print("[I] Adding video(s) to queue...")

        # Add a filename for each video from the playlist
        c = 0
        for video in parsed_video_list:
            # If tag data was provided, prepare it for adding to the videos tuple
            if tag_data_file != None:
                video_metadata = parsed_tag_data[c]
            else:
                # If not, create a variable to act as a placeholder
                video_metadata = None
                
            # Combine the download subdirectory and title to create the filename
            video_filename = os.path.join(playlist_download_directory, "{}.mp3".format(video[1]))

            # Build the tuple and add to queue
            current_video = (video[0], video[1], video_filename, video_metadata)
            video_queue.append(current_video)
 
            # Output message
            print("\t[i] \"{}\" added to queue.".format(video[1]))

            c += 1

    # Output message
    print("[I] {} videos have been added to the queue.".format(len(video_queue)))
        
    print("#######################")
    print("#  STARTING DOWNLOAD  #")
    print("#######################")
    print("##> Download Location: {}".format(outdir))
    print("##> Video Count: {}".format(len(video_queue)))
    
    # Verbose output
    if verbosity == True:
        print("####>>")
        print("[DEBUG] Videos in queue:")
        
        for video in video_queue:
            print("\t[d] {0} ({1})".format(video[0], video[1]))
        print("####>>")
        
    print("#######################")


    # Download all videos in the queue
    process_queued_videos(verbosity, use_threading, download_manager, video_queue)

# Begin execution
if __name__ == "__main__":
    main(sys.argv[1:])
