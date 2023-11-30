# lib/tag_editor.py
# Edit tags of downloaded MP3 files

import eyed3

class Editor(object):
  """ Edit tags of downloaded MP3 files

  Methods:
    __init__() - Initialize the object
    add_tags() - Add tags to an MP3 file
  """

  def __init__(self, verbosity):
    """ Initialize the object

    Arguments:
      self - self - This object
      verbosity - bool - Verbose output
    """

    self.verbosity = verbosity

  def add_tags(self, mp3_file, tag_info):
    """ Add tags to an MP3 file

    Arguments:
      self - self - This object
      mp3_file - string - Path to MP3 file
      tag_info - tuple - Tag info to add
    """
    
    """ Tag information must be passed as a tuple with the following format:
    (artist, title, album, genre)"""

    # Verbose output
    if self.verbosity == True:
      print("[DEBUGGING] Adding tags to {}...".format(mp3_file))

    # Load the file and initialize the tags
    song = eyed3.load(mp3_file)
    eyed3.log.setLevel("ERROR")
    song.initTag()
    

    # Add the tags
    song.tag.artist = tag_info[0].strip("][")
    song.tag.title = tag_info[1].strip("][")
    song.tag.album = tag_info[2].strip("][")
    song.tag.genre = tag_info[3].strip("][")


    
    # Verbose output
    if self.verbosity == True:
      print("\t[i] Artist: {}".format(str(song.tag.artist).strip('"')))
      print("\t[i] Title: {}".format(str(song.tag.title).strip('""')))
      print("\t[i] Album: {}".format(str(song.tag.album).strip('"')))
      print("\t[i] Genre: {}".format(str(song.tag.genre).strip('"')))