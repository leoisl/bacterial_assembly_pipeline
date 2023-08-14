import os
import glob
import argparse

def rename_files(base_dir):
    # Iterate over all batch folders
    for batch_dir in glob.glob(os.path.join(base_dir, "batch_*")):
        # Iterate over all files in the batch folder
        for old_filename in os.listdir(batch_dir):
            if old_filename.endswith('.contigs.fa.gz'):
                new_filename = "ilmn-" + old_filename
                old_filepath = os.path.join(batch_dir, old_filename)
                new_filepath = os.path.join(batch_dir, new_filename)

                # Rename the file
                # os.rename(old_filepath, new_filename)
                print(f"{old_filepath} -> {new_filepath}")

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Rename .fa.gz files in batch directories.')
    parser.add_argument('base_dir', help='The directory containing the batch folders.')

    # Parse arguments
    args = parser.parse_args()

    # Rename files
    rename_files(args.base_dir)

if __name__ == '__main__':
    main()

