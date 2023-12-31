# lib/tag_editor.py
# Edit tags of downloaded MP3 files

import eyed3

class Editor(object):
  """ Edit tags of downloaded MP3 files

  Methods:
    __init__() - Initialize the object
    insert_metadata() - Adds provided thumbnail and tags to an MP3 file
  """

  def __init__(self, verbosity):
    """ Initialize the object

    Arguments:
      self - self - This object
      verbosity - bool - Verbose output
    """

    self.verbosity = verbosity

  def insert_metadata(self, mp3_file, metadata):
    """ Adds thumbnail and tag information to an MP3 file
    
    Arguments:
      self - self - This object
      mp3_file - filename - The file to add the metadata to
      metadata - dict - The metadata to add

    Returns:
      tagged_mp3_file - filename - Name of the tagged MP3 file
    """

    # Load the file and initialize the tags
    open_mp3_file = eyed3.load(mp3_file)
    open_mp3_file.initTag(version=(2, 3, 0))

    # If a thumbnail is present, open and read it as binary and set it
    if metadata["thumbnail"] != None:
      with open(metadata["thumbnail"], "rb") as thumbnail_file:
        raw_thumbnail = thumbnail_file.read()

      open_mp3_file.tag.images.set(3, raw_thumbnail, "image/jpeg", "cover")

    # See if any other tags are present in the metadata dictionary and set the ones that are
    if metadata["title"] != None:
      open_mp3_file.tag.title = metadata["title"]
    if metadata["artist"] != None:
      open_mp3_file.tag.artist = metadata["artist"]
    if metadata["album"] != None:
      open_mp3_file.tag.album = metadata["album"]
    if metadata["track_num"] != None:
      open_mp3_file.tag.track_num = int(metadata["track_num"])
    if metadata["recording_date"] != None:
      format_year = eyed3.core.Date(int(metadata["recording_date"]))
      open_mp3_file.tag.recording_date = format_year

    # Save the changes and return tagged file name
    open_mp3_file.tag.save()
    tagged_mp3_file = mp3_file
    return tagged_mp3_file






