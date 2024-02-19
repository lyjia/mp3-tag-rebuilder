from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3
import copy
import argparse

def rebuild_id3_tags(file_path):
    # Load the MP3 file
    audio = MP3(file_path, ID3=ID3)

    # Copy existing tags
    try:
        tags = copy.deepcopy(audio.tags)
    except error as e:
        print(f"Error reading ID3 tags: {e}")
        return

    # Delete existing tags
    audio.delete()
    audio.save()

    # Re-add copied tags to the file
    audio = MP3(file_path, ID3=ID3)
    audio.tags = tags

    # Save the changes
    audio.save()

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Rebuild ID3 tags of an MP3 file.")

    # Add the arguments
    parser.add_argument('file_path', type=str, help="The path to the MP3 file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    rebuild_id3_tags(args.file_path)