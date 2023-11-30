# lib/validator.py
# Ensure all specified file paths are valid and exist, make sure all YouTube video URLs are of valid format and do not return 404 errors, etc. 

from urllib.parse import urlparse
from pathvalidate import is_valid_filepath, sanitize_filepath
from pathvalidate import is_valid_filename, sanitize_filename
from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import AgeRestrictedError, VideoRegionBlocked, LiveStreamError, VideoPrivate, VideoUnavailable

class Validator(object):
  """ Validate file paths and URLs

  Methods:
    __init__() - Initialize the object
    sanatize_path() - Validate and sanatize a file path
    sanatize_name() - Validate and sanatize a file name
    validate_video_url() - Confirm video availability and create a YouTube object
  """

  def __init__(self, verbosity):
    """ Initialize the object

    Arguments:
      self - self - This object
      verbosity - bool - Enable verbose output
    """

    self.verbosity = verbosity

  def sanatize_path(self, file_path):
    """ Validate and sanatize a file path

    Arguments:
      self - self - This object
      file_path - string - File path to validate

    Returns:
      clean_file_path - string - Sanatized file path
    """

    # Check if specified path is invalid, and if so, sanatize it
    if is_valid_filepath(file_path) == False:
      clean_file_path = sanatize_filepath(file_path)

      # Verbose output
      if self.verbosity == True:
        print("[DEBUGGING] File path required sanatization, is now {}".format(clean_file_path))

    else:
        # Path good as is
        clean_file_path = file_path

    return clean_file_path

  def sanatize_name(self, file_name):
    """ Validate and sanatize a file name

    Arguments:
      self - self - This object
      file_name - string - File name to validate

    Returns:
      clean_file_name - string - Sanatized file name
    """

    # Check if specified name is invalid, if so, sanatize it
    if is_valid_filename(file_name) == False:
      clean_file_name = sanatize_filename(file_name)

      # Verbose output
      if self.verbosity == True:
        print("[DEBUGGING] File name required sanatization, is now {}".format(clean_file_name))

    else:
      # Name good as is
      clean_file_name = file_name

    return clean_file_name

  def validate_video_url(self, video_url):
    """ Confirm video availabilty and return a YouTube object

    Arguments:
      self - self - This object
      video_url - string - The URL of the video

    Returns:
      validated_video - YouTube object - The validated video object
    """

    # First, confirm that the argument passed by the user is a valid URL
    test = urlparse(video_url)
    if all([test.scheme, test.netloc]) == True:
      # Now attempt to create a YouTube object, accounting for possible reasons the video would be unavailable
      try:
        validated_video = YouTube(video_url, on_progress_callback=on_progress)

      except AgeRestrictedError as err_msg:
        raise Exception("Video is age restricted and cannot be accessed")

      except VideoRegionBlocked as err_msg:
        raise Exception("Video is blocked in your region")

      except LiveStreamError as err_msg:
        raise Exception("Cannot download video because it is a livestream")

      except VideoPrivate as err_msg:
        raise Exception("This video is private")

      except VideoUnavailable as err_msg:
        raise Exception(err_msg)

      return validated_video

    else:
      print("[ERROR] {} is not a valid URL".format(video_url))
      exit(0)

    

