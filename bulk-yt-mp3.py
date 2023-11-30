#!/usr/bin/python3

"""
Bulk YouTube to MP3
A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos or entire playlists. By default, all downloads are stored in the users home directory. 

Version 1.2
By Brandon REDACTED
"""

import os
import sys
import time
import getopt
import threading
from lib import manager
from lib import validator
from lib import tag_editor

def process_queued_videos(verbosity, use_threading, add_tags, download_manager, data_validator, video_queue, tag_info_list):
    """ Download all queued videos and create threads if enabled

    Arguments:
        verbosity - bool - Verbose output
        use_threading - bool - Use multithreading
        add_tags - bool - Says whether to add tags or not
        download_manager - Manager object - Download management tool
        data_validator - Validator object - Data validation too
        video_queue - list of tuples - A list of video url/title/filename tuples
        tag_info_list - list of tuples - Tag information
    """

    # Create a new tag editor, if applicable
    if add_tags == True:
        metadata_editor = tag_editor.Editor(verbosity)

    # If multithreading is enabled
    if use_threading == True:
        # Initialize a list of all threads
        thread_list = []

        # Output message
        print("[I] Generating download threads...")

        # Initialize a list to associate file names and tag info, if applicable
        if add_tags == True:
            file_tag_list = []
        
        # Create a new thread for each video and add it to the list
        c = 0
        for video in video_queue:
            new_thread = threading.Thread(target=download_manager.download_single_video, args=(video[0], video[2]))
            thread_list.append(new_thread)

            # Append the resulting filename and its tag info to the list, if applicable
            if add_tags == True:
                tag_info = tag_info_list[c].strip("[]").split(";")
                file_tag_list.append((video[2], tag_info))  
            c = c + 1

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

        # Add tags, if applicable
        if add_tags == True:
            for next_file in file_tag_list:
                metadata_editor.add_tags(next_file[0], next_file[1])

    else:
        # Download normally
        print("[I] Downloads now in progress...")
        c = 0
        for video in video_queue:
            print("\t[i] Downloading {0} ({1})".format(video[1], video[0]))
            download_manager.download_single_video(video[0], video[2])

            if add_tags == True:
                # Convert the tag info back into a list
                tag_info = tag_info_list[c].strip("[]").split(";")

                # Add tags
                metadata_editor.add_tags(video[2], tag_info)
            c = c + 1
            
        
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

    """ Bebop is high as shit and likes to be extra, enable this to add a purely aesthetic wait/input to the UI that just makes it look cooler. Any sane person has this set to False.
    """
    bebops_vain_ui_enhancements = False

    # Set variables with default values
    verbosity = False
    use_threading = False
    outdir = "{}/".format(os.getenv("HOME"))
    video_urls = []
    playlist_url = None
    add_tags = False
    tag_info = None

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
            print("Version 1.2")
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
            add_tags = True
            tag_info = arg

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
    print("#######################")
    print("# Bulk YouTube to MP3 #")
    print("# Version 1.2         #")
    print("#######################")
    print("[I] Initializing program...")

    # Create a new instance of the data validator
    data_validator = validator.Validator(verbosity)

    # Sanatize the output directory if it is not the default
    if outdir != "{}/".format(os.getenv("HOME")):
        # Make sure the last character is a slash, and if not, append one
        if outdir.endswith("/") == False:
            fixed_outdir = outdir + "/"
            outdir = fixed_outdir
        
        # Verbose output
        if verbosity == True:
            print("[DEBUGGING] Sanatizing user specified output directory...")

        outdir = data_validator.sanatize_path(outdir)
    
    # Initialize a new download manager
    download_manager = manager.DownloadManager(verbosity, data_validator)

    # Specify the download location
    download_manager.change_output_directory(outdir)

    # Tell the user where the output directory is
    print("[I] Output directory set to: {}".format(outdir))

    # Initialize the video queue
    video_queue = []

    # Handle individual videos and add them to the queue
    if len(video_urls) > 0:
        # Output message
        print("[I] Adding video(s) to queue...")
        
        for video_url in video_urls:
            # Get the video title
            video_title = download_manager.get_video_title(video_url)

            # Create the URL/title tuple for and add the video to the queue
            current_vid = (video_url, video_title, "{}.mp3".format(video_title))
            video_queue.append(current_vid)

            # Output message
            print("\t[i] \"{0}\" added to queue.".format(video_title))


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
        parsed_video_list = download_manager.parse_playlist(playlist_url, playlist_download_directory)

        # Tell the user how many videos are in the playlist and where the outdir is
        print("[I] Number of videos in playlist: {}".format(len(parsed_video_list)))
        print("[I] Download location for playlist videos: {}".format(playlist_download_directory))
        print("[I] Adding video(s) to queue...")
        
        for playlist_video in parsed_video_list:
            video_queue.append(playlist_video)

            # Output message
            print("\t[i] \"{}\" added to queue.".format(playlist_video[1]))

    # Output message
    print("[I] {} videos have been added to the queue.".format(len(video_queue)))

    # Load tag info
    with open(tag_info, "r") as f:
        tag_info_list = f.readlines()

    # If the user wants to humor Bebops vanity
    if bebops_vain_ui_enhancements == True:
        print("[I] Finalizing queue...")
        time.sleep(3)
        print("\t[i] ...Done. Ready to begin downloads.")
        print("")
        input("[***] Press [ENTER] to initiate download) [***]")
        os.system("clear")

    else:
        print("")
        
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

    # If its enabled, Bebops vanity continues
    if bebops_vain_ui_enhancements == True:
        time.sleep(1)

    # Download all videos in the queue
    process_queued_videos(verbosity, use_threading, add_tags, download_manager, data_validator, video_queue, tag_info_list)

# Begin execution
if __name__ == "__main__":
    main(sys.argv[1:])
