import argparse
from mutagen.id3 import ID3, error, ID3NoHeaderError
from mutagen.mp3 import MP3

VERSION = '0.0'

medieval_system = {
    '1A': 'Abm',
    '1B': 'Bmaj',
    '2A': 'Ebm',
    '2B': 'F#maj',
    '3A': 'Bbm',
    '3B': 'Dbmaj',
    '4A': 'Fm',
    '4B': 'Abmaj',
    '5A': 'Cm',
    '5B': 'Ebmaj',
    '6A': 'Gm',
    '6B': 'Bbmaj',
    '7A': 'Dm',
    '7B': 'Fmaj',
    '8A': 'Am',
    '8B': 'Cmaj',
    '9A': 'Em',
    '9B': 'Gmaj',
    '10A': 'Bm',
    '10B': 'Dmaj',
    '11A': 'F#m',
    '11B': 'Amaj',
    '12A': 'C#m',
    '12B': 'Emaj'
}
medieval_system_inverse = {v: k for k, v in medieval_system.items()}


def log(msg):
    print(msg)


def rebuild_id3_tags(file_path, convert_keys=False, strip_ufid=False):
    try:
        audio = MP3(file_path, ID3=ID3)
    except ID3NoHeaderError:
        log(f"No ID3 tag found in {file_path}")
        return

    new_tags = ID3()

    for tag, value in audio.tags.items():
        if convert_keys:
            if tag=='TKEY' and value.text[0] in medieval_system_inverse:
                newval = medieval_system_inverse[value.text[0]]
                log(f"Converting {tag}: {value.text[0]} --> {newval}...")
                value.text = [newval]

        if strip_ufid:
            if tag=="UFID":
                log(f"Stripping {tag}...")
                continue

        # Directly add the frame to the new tag
        log(f"Copying {tag}: {str(value)[:64]}")
        new_tags.add(value)

    audio.delete()  # Remove existing tags
    audio.save()  # Save the changes
    log(f"Destroyed existing ID3 tags for {file_path}")

    audio.tags = new_tags  # Assign new tags
    audio.save()  # Save the changes
    log(f"ID3 tags successfully rebuilt for {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Rebuild ID3 tags of an MP3 file. (Version {VERSION})")
    parser.add_argument('file_path', type=str, help="The path to the MP3 file")
    parser.add_argument('--convert-keys', '-c', action='store_true', help="Convert abbreviated musical keys (e.g. "
                                                                          "'Fmaj') to a certain medieval-themed notation system (e.g. '7B').")
    parser.add_argument('--strip-pii', '-s', action='store_true', help="Strip tags from Beatport containing "
                                                                       "identifying information.")

    args = parser.parse_args()

    rebuild_id3_tags(args.file_path,
                     convert_keys=args.convert_keys,
                     strip_ufid=args.strip_ufid)
