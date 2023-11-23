# lib/manager.py
# Handle all tasks related to downloading

import os
import sys
import csv
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoRegionBlocked

class DownloadManager(object):
    """ Handle all tasks related to downloading

    Methods:
        __init__() - Initialize the object
        change_output_directory() - Change download location
        get_video_title() - Get the title of a video
        get_playlist_title() - Get the title of a playlist
        dowload_single_video() - Download a single video
        parse_playlist() - Parse a playlist to download from
    """

    def __init__(self, verbosity):
        """ Initialize the object

        Arguments:
            self - self - This object
            verbosity - bool - Enable verbose output
        """

        self.verbosity = verbosity

    def change_output_directory(self, outdir):
        """ Change download location
        
        Arguments:
            self - self - This object
            outdir - string - Directory to output to
        """

        # Verbose output
        if self.verbosity == True:
            print("[DEBUGGING] Setting output directory to {}".format(outdir))

        self.outdir = outdir

    def get_video_title(self, video_url):
        """ Get the title of a video
        
        Arguments:
            self - self - This object
            video_url - string - The URL of the video
            
        Returns:
            video_title - string - The title of the video
        """

        video = YouTube(video_url)
        video_title = video.title

        # Verbose output
        if self.verbosity == True:
            print("[DEBUGGING] Title of {0} is {1}".format(video_url, video_title))
            
        return video_title

    def get_playlist_title(self, playlist_url):
        """ Get the title of a playlist
        
        Arguments:
            self - self - This object
            playlist_url - string - The URL of the playlist
            
        Returns:
            playlist_title - string - The title of the playlist
        """

        playlist = Playlist(playlist_url)
        playlist_title = playlist.title

        # Verbose output
        if self.verbosity == True:
            print("[DEBUGGING] Title of {0} is {1}".format(playlist_url, playlist_title))
            
        return playlist_title
    

    def download_single_video(self, video_url, file_name):
        """ Download the MP3 file of a video

        Arguments:
            self - self - This object
            video_url - string - URL of the video
            file_name - string - Name for the MP3 file
        """

        # Full path to new MP3 file
        file_path = "{0}{1}".format(self.outdir, file_name)

        # Verbose output
        if self.verbosity == True:
            print("[DEBUGGING] Full path of new file: {}".format(file_path))

        # Attempt to download the MP3 file
        try:
            video = YouTube(video_url, on_progress_callback=on_progress)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(filename=file_path)

        except KeyError as err_msg:
            raise Exception(err_msg)
    
    def parse_playlist(self, playlist_url):
        """ Parse a playlist to download from
        
        Arguments:
            self - self - This object
            playlist_url - string - URL to playlist

        Returns:
            video_list - list - A list of video url/name tuples
        """

        video_list = []

        # Create a new playlist object
        playlist = Playlist(playlist_url)
        
        # Get the video urls
        video_urls = playlist.video_urls

        # Verbose output
        if self.verbosity == True:
            print("[DEBUGGING] Number of videos in playlist: {}".format(len(playlist.videos)))

        # Loop through all the videos individually to create url/name tuples to append to video list
        c = 0
        for video in playlist.videos:
            current_video = (video_urls[c], "{}.mp3".format(video.title))
            video_list.append(current_video)

        return video_list

    

            



