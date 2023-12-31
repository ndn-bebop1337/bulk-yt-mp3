# lib/manager.py
# Handle all tasks related to downloading

import os
import subprocess
import csv
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoRegionBlocked

class DownloadManager(object):
    """ Handle all tasks related to downloading and building the video queue

    Methods:
        __init__() - Initialize the object
        get_video_title() - Get the title of a video
        get_playlist_title() - Get the title of a playlist
        parse_tag_data_file() - Parse a CSV file of MP3 metadata
        parse_playlist() - Parse a playlist to download from
        download() - Download a YouTube video as audioless MP4
        convert() - Convert a downloaded video to MP3 format
    """

    def __init__(self, verbosity):
        """ Initialize the object

        Arguments:
            self - self - This object
            verbosity - bool - Enable verbose output
            data_validator - Validator object - Data validation tool
        """

        self.verbosity = verbosity

    def get_video_title(self, video_url):
        """ Get the title of a video
        
        Arguments:
            self - self - This object
            video_url - string - The URL of the video
            
        Returns:
            video_title - string - The title of the video
        """

        video = YouTube(video_url, on_progress_callback=on_progress)
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

    def parse_tag_data_file(self, tag_data_file):
        """ Parse a CSV file of MP3 metadata
        
        Arguments:
            self - self - This object
            tag_data_file - string - The path to the CSV file
            
        Returns:
            parsed_tag_data - list of dicts - Parsed MP3 metadata
        """

        # Initialize the list of tag data dictionaries
        parsed_tag_data = []
        
        # Open the CSV file and read it row by row
        with open(tag_data_file) as open_tag_data_file:
            # Initialize the CSV reader
            csv_reader = csv.reader(open_tag_data_file, delimiter=",")

            for row in csv_reader:
                # Check cell-by-cell for empty strings and replace them with Nonetype
                d = 0
                for cell in row:
                    if cell == "":
                        row[d] = None
                    d += 1

                # Build a dictionary from this rows data and append it to the list
                row_data = {
                    "thumbnail": row[0],
                    "title": row[1],
                    "artist": row[2],
                    "album": row[3],
                    "track_num": row[4],
                    "genre": row[5],
                    "recording_date": row[6]
                }
                parsed_tag_data.append(row_data)

            # Return the list of tag data dictionaries
            return parsed_tag_data

    def parse_playlist(self, playlist_url):
        """ Parse a playlist and retrieve from it a list of video URLs and titles

        Arguments:
            self - self - This object
            playlist_url - string - URL of the YouTube playlist

        Returns:
            video_list - list of tuples - A list of video URL/title tuples
        """

        # Initialize the video list
        video_list = []

        # Create a new playlist object
        playlist = Playlist(playlist_url)

        # Get the video urls
        video_urls = playlist.video_urls

        # Loop through all the videos, adding their URL and title to the list
        c = 0
        for video in playlist.videos:
            current_video = (video_urls[c], video.title)
            video_list.append(current_video)

        # Return the list of videos
        return video_list
        

    def download(self, video_url, new_file_name):
        """ Download a YouTube video as audioless MP4 to the filepath specified
        
        Arguments:
            self - self - This object
            video_url - string - URL of the YouTube video to download
            new_file_name - filename - The desired name of the new file

        Returns:
            downloaded_file - filename - The name of the newly downloaded file
        """

        # Attempt to create a YouTube object for the video, taking into account and handling any YouTube related reasons that the video might be unavailable for download
        try:
            video = YouTube(video_url, on_progress_callback=on_progress)

        # If video is age restricted
        except AgeRestrictedError as err_msg:
            raise Exception("Video is age restricted and cannot be accessed")

        # If video is region blocked
        except VideoRegionBlocked as err_msg:
            raise Exception("Video is blocked in your region")

        # If video is a livestream
        except LiveStreamError as err_msg:
            raise Exception("Cannot download video because it is a livestream")

        # If video is private
        except VideoPrivate as err_msg:
            raise Exception("This video is private")

        # If video is unavailable for any other reason
        except VideoUnavailable as err_msg:
            raise Exception(err_msg)

        # Find an audio only stream for the video and download it
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=new_file_name)

        # Verify that the file did indeed download and return the new files name
        if os.path.isfile(new_file_name) == True:
            downloaded_file = new_file_name
            return downloaded_file

    def convert(self, old_file_name, new_file_name):
        """ Convert an audioless MP4 file to the MP3 format
        
        Arguments:
            self - self - This object
            old_file_name - filename - The name of the file to convert
            new_file_name - filename - The name for the newly converted file

        Returns:
            converted_file - filename - The name of the newly converted file
        """

        # Build a command that uses the ffmpeg utility to facilitate conversion
        command = """ffmpeg -hide_banner -loglevel error -i "{0}" "{1}" """.format(old_file_name, new_file_name)

        # Run the command
        subprocess.check_output(command, shell=True)

        # Verify that the converted file was created and return
        if os.path.isfile(new_file_name) == True:
            converted_file = new_file_name
            return converted_file

class Downloader(object):
    """ Unifies downloading and conversion into one object method
    
    Methods:
        __init__() - Initialize the object
        download_and_convert() - Download and convert a video
    """

    def __init__(self, download_manager, editor):
        """ Initialize the object
        
        Arguments:
            self - self - This object
            download_manager - DownloadManager object - The manager object used to download and convert videos
            editor - Editor object - Tag editor for inserting MP3 metadata
            """

        self.download_manager = download_manager
        self.editor = editor

    def download_and_convert(self, video_url, video_title, video_filename, video_metadata):
        """ Download and convert a video in a unified manner, inserting metadata if present
        
        Arguments:
            self - self - This object
            video_url - string - URL of the YouTube video to download
            video_title - string - Title of the video
            video_filename - filename - The desired filename for the downloaded video
            video_metadata - dict or None - Either provided tag data or Nonetype

        Returns:
            mp3_file - filename - The resultant MP3 format file
        """

        # Create a temporary filename for the preconversion download and begin download
        temp_video_filename = video_filename + ".temp"
        downloaded_file = self.download_manager.download(video_url, temp_video_filename)

        # Convert the downloaded file to the MP3 format
        converted_file = self.download_manager.convert(downloaded_file, video_filename)

        # Remove the temporary file
        os.remove(downloaded_file)

        # If metadata was provided, insert it into the new MP3 file
        if video_metadata != None:
            tagged_mp3_file = self.editor.insert_metadata(converted_file, video_metadata)

        # Return the new MP3 files name
        mp3_file = converted_file
        return mp3_file

        

        

        

    

            



