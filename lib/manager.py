# lib/manager.py
# Handle all tasks related to downloading

import os
import sys
import csv
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress

class DownloadManager(object):
    """ Handle all tasks related to downloading

    Methods:
        __init__() - Initialize the object
        parse_playlist() - Parse a playlist to download from
        parse_csv() - Parse a CSV file to download from
        download_mp3() - Download the MP3 of a video
    """

    def __init__(self, outdir):
        """ Initialize the object

        Arguments:
            self - self - This object
            outdir - string - Directory to output to
        """

        # See if an output directory was specified, if not, use cwd
        if outdir == None:
            self.outdir = os.getcwd()

        else:
            if os.path.exists(outdir) == False:
                raise Exception("Directory does not exist")
            else:
                self.outdir = outdir

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

        # Loop through all the videos individually to create url/name tuples to append to video list
        c = 0
        for video in playlist.videos:
            current_video = (video_urls[c], "{}.mp3".format(video.title))
            video_list.append(current_video)

        return video_list

    def parse_csv(self, csv_file):
        """ Parse a CSV file to download from
        
        Arguments:
            self - self - This object
            csv_file - string - Path to CSV file

        Returns:
            video_list - list - A list of video url/name tuples
        """

        video_list = []
       
        # Make sure file exists
        if os.path.isfile(csv_file) == False:
            raise Exception("File does not exist: {}".format(csv_file))

        # Open the CSV file
        with open(csv_file) as open_csv:
            csv_reader = csv.reader(open_csv, delimiter=",")

            # Extract the video URL and file name row by row, then append into tuples to be added to video_list
            for row in csv_reader:
                current_video = (row[0], row[1])
                video_list.append(current_video)

        return video_list

    def download_mp3(self, video_url, file_name):
        """ Download the MP3 file of a video

        Arguments:
            self - self - This object
            video_url - string - URL of the video
            file_name - string - Name for the MP3 file
        """

        # Full path to new MP3 file
        file_path = "{0}{1}".format(self.outdir, file_name)

        # Attempt to download the MP3 file
        try:
            video = YouTube(video_url, on_progress_callback=on_progress)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(filename=file_path)

        except KeyError as err_msg:
            raise Exception(err_msg)

            



