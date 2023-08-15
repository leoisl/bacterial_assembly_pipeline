import argparse
import os
import json
import pandas as pd

def load_metadata_from_file(filepath):
    """Load metadata from a given JSON file."""
    print(f"Loading metadata from {filepath}")
    with open(filepath, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data["ena_metadata"])

def crawl_directory_for_metadata(directory):
    """Crawl a given directory for metadata.json files and load them into a DataFrame."""
    frames = []

    # Walk through each directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == "metadata.json":
                filepath = os.path.join(dirpath, filename)
                frames.append(load_metadata_from_file(filepath))

    return pd.concat(frames, ignore_index=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl directories for metadata.json and load them into a DataFrame.")
    parser.add_argument('directory', type=str, help='The root directory to start crawling from.')
    parser.add_argument('output_tsv', type=str, help='Path to the output TSV file.')
    args = parser.parse_args()

    df = crawl_directory_for_metadata(args.directory)
    df.to_csv(args.output_tsv, sep='\t', index=False)
    print(f"Data saved to {args.output_tsv}")
