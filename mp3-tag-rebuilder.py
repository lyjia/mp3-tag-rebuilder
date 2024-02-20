import argparse, os, glob, time
from mutagen.id3 import ID3, error, ID3NoHeaderError, COMM, TKEY, UFID
from mutagen.mp3 import MP3

VERSION = '0.2.1'

medieval_system = {
    '1A': ['Abmin', 'G#min', 'Abm', 'G#m'],
    '1B': ['Bmaj'],
    '2A': ['Ebmin', 'D#min', 'Ebm', 'D#m'],
    '2B': ['F#maj', 'Gbmaj'],
    '3A': ['Bbmin', 'A#min', 'Bbm', 'A#m'],
    '3B': ['Dbmaj', 'C#maj'],
    '4A': ['Fmin', 'Fm'],
    '4B': ['Abmaj', 'G#maj'],
    '5A': ['Cmin', 'Cm'],
    '5B': ['Ebmaj', 'D#maj'],
    '6A': ['Gmin', 'Gm'],
    '6B': ['Bbmaj', 'A#maj'],
    '7A': ['Dmin', "Dm"],
    '7B': ['Fmaj'],
    '8A': ['Amin', 'Am'],
    '8B': ['Cmaj'],
    '9A': ['Emin', 'Em'],
    '9B': ['Gmaj'],
    '10A': ['Bmin', 'Bm'],
    '10B': ['Dmaj'],
    '11A': ['F#min', 'Gbmin', 'F#m', 'Gbm'],
    '11B': ['Amaj'],
    '12A': ['C#min', 'Dbmin', 'C#m', 'Dbm'],
    '12B': ['Emaj']
}

# Invert the dictionary and flatten the list of equivalent keys
medieval_system_inverse = {k2: k for k, v in medieval_system.items() for k2 in v}


def log(msg):
    print(msg)


def get_mp3_files(path):
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        mp3_files = glob.glob(os.path.join(path, '*.mp3'))
        log(f"Processing folder {path} containing {len(mp3_files)} file(s)...")
        return mp3_files
    else:
        print(f"Path {path} does not exist!")
        exit(-1)


def rebuild_id3_tags(file_path, convert_key=False, strip_ufid=False):
    try:
        audio = MP3(file_path, ID3=ID3)
        log(f"Processing file {file_path}...")
    except ID3NoHeaderError:
        log(f"No ID3 tag found in {file_path}")
        return

    new_tags = ID3()

    for tag, value in audio.tags.items():
        if convert_key and tag == 'TKEY':
            if value.text[0] in medieval_system_inverse:
                newval = medieval_system_inverse[value.text[0]]
                log(f"Converting {tag}: {value.text[0]} --> {newval}...")
                value.text = [newval]
            else:
                log(f"Key {value.text[0]} not recognized!")

        if strip_ufid:
            if tag == 'UFID':
                log(f"Stripping {tag}...")
                continue

        # Directly add the frame to the new tag
        log(f"Copying {tag}: {str(value)[:64]}")
        new_tags.add(value)

    audio.delete()  # Remove existing tags
    audio.save()  # Save the changes
    log(f"Destroyed existing ID3 tags for {file_path}")
    time.sleep(1) # wait for the filesystem to catch up

    audio.tags = new_tags  # Assign new tags
    audio.save()  # Save the changes
    log(f"ID3 tags rebuilt for {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Rebuild ID3 tags of an MP3 file. (Version {VERSION})")
    parser.add_argument('file_path', type=str, help="The path to the MP3 file, or a folder of mp3 files.")
    parser.add_argument('--convert-key', '-c', action='store_true', help="Convert abbreviated musical keys (e.g. "
                                                                          "'Fmaj') to a certain medieval-themed notation system (e.g. '7B').")
    parser.add_argument('--strip-ufid', '-s', action='store_true', help="Strip tags from Beatport containing "
                                                                       "identifying information.")
    args = parser.parse_args()

    all_files = get_mp3_files(args.file_path)

    for file_path in all_files:
        rebuild_id3_tags(file_path,
                         convert_key=args.convert_key,
                         strip_ufid=args.strip_ufid)
