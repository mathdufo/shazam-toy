import argparse

from identification.identify import (identify_file,
                                     identify_microphone,
                                     print_matches)

from storage.register import register_directory
from storage.database import database

def main():
    parser = argparse.ArgumentParser(description='Toy Implementation Of Shazam Algorithm')
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    identify_parser = subparsers.add_parser('identify', help='Identify audio sample')
    identify_group = identify_parser.add_mutually_exclusive_group(required=True)
    identify_group.add_argument('-m', '--microphone', action='store_true', help='Identify from microphone')
    identify_group.add_argument('-f', '--file', type=str, help='Identify from file')
    identify_parser.add_argument('-d', '--duration', type=int, help='Duration in seconds (microphone only)')

    register_parser = subparsers.add_parser('register', help='Fill database with audio samples from directory')
    register_parser.add_argument('-wd', '--wav_directory', type=str, help='Directory path where .wav files of the samples are stored', required=True)
    register_parser.add_argument('-td', '--txt_directory', type=str, help='Directory path where .txt files containing info about the samples are stored')
    args = parser.parse_args()

    db = database()

    if args.command == 'identify':
        if args.microphone:
            if args.duration is None or args.duration <= 0:
                parser.error("When using the microphone, duration bigger than 0 is required.")

            while True:
                print(f"***RECORDING FOR {args.duration} SECONDS***")
                matches = identify_microphone(db, args.duration)
                print_matches(matches)

        else:
            matches = identify_file(db, args.file)
            print_matches(matches)

    elif args.command == 'register':
        print("This could take a very long time")
        register_directory(db, args.wav_directory, args.txt_directory)


if __name__ == "__main__":
    main()