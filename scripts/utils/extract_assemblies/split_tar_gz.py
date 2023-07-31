import os
import argparse
from pathlib import Path

def write_filepaths(dir_path, output_file_base, max_entries):
    output_file_no = 0
    output_file = create_and_open_file(f"{output_file_base}_{output_file_no}.txt")
    entries_counter = 0

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.tar.gz'):
                output_file.write(os.path.join(root, file) + "\n")
                entries_counter += 1

                if entries_counter >= max_entries:
                    output_file.close()
                    output_file_no += 1
                    output_file = create_and_open_file(f"{output_file_base}_{output_file_no}.txt")
                    entries_counter = 0
    output_file.close()

def create_and_open_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, 'w')

def main():
    parser = argparse.ArgumentParser(description="Write paths of .tar.gz files to .txt files")
    parser.add_argument('-d', '--dir_path', required=True, help="Directory to process")
    parser.add_argument('-o', '--output_file_base', required=True, help="Base name of the output .txt files")
    parser.add_argument('-n', '--max_entries', type=int, required=True, help="Maximum number of entries per .txt file")
    args = parser.parse_args()

    dir_path = Path(args.dir_path)
    output_file_base = args.output_file_base
    max_entries = args.max_entries

    write_filepaths(dir_path, output_file_base, max_entries)


if __name__ == "__main__":
    main()
