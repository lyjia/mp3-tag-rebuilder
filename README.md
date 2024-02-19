# MP3TagRebuilder

MP3TagRebuilder is a python script that fixes a very specific type of corrupted MP3 ID3 tag that seems to appear rather often with purchases from Beatport.

This particular defect somehow prevents Serato from saving track, key, and BPM analyses to the MP3's ID3 header. When this happens, Serato will seemingly analyze the MP3 file perfectly fine, but then when it is reloaded, analysis isn't present (notice how the track preview fills in slowly from left-to-right, as opposed to appearing instantly), and the data in the BPM and Key columns revert to the previous values provided by Beatport.

This script has some additional features that I have added, that enhance my own personal music intake workflow:

* `--convert-key` will convert the musical key notation that Beatport provides into a certain medieval-themed key notation system. You know the one I'm talking about, it has the rainbow wheel that we've all seen. With this switch, "Fmaj" is instead written as "7B"
* `--strip-ufid` will strip the UFID field from the rebuilding process

## How to Use

As this is a python script, it requires that you have a python interpreter installed and ready-to-go. I wrote this with Python 3.10, but any version of Python 3 should work. If in doubt, install the latest version.

### Install the Prerequisites

This only needs to be done before first-use. Run the following from within the script's folder:

`pip install -r requirements.txt`

### Get Help and Usage Info

The `--help` switch prints a detailed command-line reference.

`python mp3-tag-rebuilder.py --help`,

### Rebuild Tags for a Single File

To rebuild the tags for a single file, run the following:

`python mp3-tag-rebuilder.py /path/to/a_file.mp3`, replacing "/path/to/a_file.mp3" with your own file path.