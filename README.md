# MP3TagRebuilder

MP3TagRebuilder is a python script designed to fix a very specific type of corrupted MP3 ID3 tag that seems to appear rather often with purchases from Beatport.

This particular defect somehow prevents Serato from saving track, key, and BPM analyses to the MP3's ID3 header. When this happens, Serato will seemingly analyze the MP3 file perfectly fine, but then when it is reloaded, analysis isn't present (notice how the track preview fills in slowly from left-to-right, as opposed to appearing instantly), and the data in the BPM and Key columns revert to the previous values provided by Beatport.

This script has some additional features that I have added, that enhance my own personal music intake workflow:

* `--convert-key` will convert the musical key notation that Beatport provides into a certain medieval-themed key notation system. You know the one I'm talking about, it has the rainbow wheel that we've all seen. With this switch, "Fmaj" is instead written as "7B"
* `--strip-ufid` will strip the UFID field from the rebuilding process

## WARNING!

This script DESTRUCTIVELY modifies files that are passed to it! It could potentially screw up your mp3 files or your DJ software's database! *YOU* are responsible for any damage suffered as a result of its use! YOU'VE BEEN WARNED!!!

**USE THIS SOFTWARE AT YOUR OWN RISK!** See the License section below for more information.

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

## Note About Tracks Already Imported to Serato

Serato seems to cache ID3 tags to an internal database and seems to use that to accelerate track display in the file browser. It will not re-read ID3 tags until a given track is selected and cued, and it doesn't seem to update its internal database with this information.

Rather frustratingly, the data it caches seems to also carry this corruption and it will ignore new ID3 data even if you re-run analysis, which will make it seem as if this script does nothing. 

The only way I've figured out to get Serato to purge this cache is to make it think the file is deleted, after which Serato forget any information it has saved on it.

To do this workaround:

1. Process the file with MP3TagRebuilder per the instructions above.
1. Rename the file on your filesystem (from something like 'mysong.mp3' to 'mysong2.mp3', then cue it up in Serato. This will cause Serato to think the file is missing, and it deletes its cache for that file. The file will display as yellow with just its filename in Serato's file browser. 
1. Then, rename the file back to its original filename and cue it up again. Serato will perform its analysis and save the updated ID3 tags to its cache.
1. Subsequent uses of the given track will behave as expected, with the track preview appearing instantly and all metadata being correct.

## License:

The MIT License

Copyright © 2010-2016 Mitchell Hashimoto

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
