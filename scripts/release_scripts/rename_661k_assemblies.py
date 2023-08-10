import os
import glob
import argparse

def rename_files(base_dir):
    # Iterate over all batch folders
    for batch_dir in glob.glob(os.path.join(base_dir, "batch_*")):
        # Iterate over all .fa.gz files in the batch folder
        for old_filename in glob.glob(os.path.join(batch_dir, "*.contigs.fa.gz")):
            # Create the new filename by replacing '.' with '_'
            new_filename = old_filename.replace('.contigs.fa.gz', '_contigs.fa.gz')
            # Rename the file
            os.rename(old_filename, new_filename)
            print(f"{old_filename} -> {new_filename}")

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

