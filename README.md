# Bulk YouTube To MP3
## Version 1.2
## By Brandon REDACTED
---
### About
A tool for the bulk downloading of YouTube videos as MP3 files. It has the capability to download either individual videos, a list of videos, or even entire playlists. By default, all downloads are stored in the users home directory, however this can be changed with the `-o` or `--outdir` command line arguments. Bulk YouTube to MP3 is powered by the [PyTube](https://pytube.io/en/latest/index.html) module, credit and thanks to the people behind it for making this project possible.

### Basic Usage
**Downloading Single Videos**

To download a single video, use the `-s` or `--single` command line argument, like so:

`$ python bulk-yt-mp3.py -s https://www.youtube.com/watch?v=mPf4v9LGF30`

Alternatively, you can download multiple individual videos by passing them as standalone arguments to the program:

`$ python bulk-yt-mp3.py https://www.youtube.com/watch?v=mPf4v9LGF30 https://www.youtube.com/watch?v=NmQN635Rheo`

**Downloading Whole Playlists**

If you want to download all of the videos in a playlist, you can use the `-p` or `--playlist` options:

`$ python bulk-yt-mp3.py --playlist https://www.youtube.com/playlist?list=PL6ogdCG3tAWhsK5KnK39gtx3xYZngN-EV`

**Additional Information**

More details about the programs functionality and usage can be found in the built in help menu, which can be accessed with `-h` or `--help`, like so:

`$ python bulk-yt-mp3.py -h`

### Credit
**Developed by** Brandon REDACTED, AKA Bebop to all my IRL homies

Thank you to Bones, for providing an endless supply of high quality emotional support, and to methamphetamine, for keeping me awake and focused. 