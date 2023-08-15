import argparse
import pandas as pd
import os

# Define the CLI argument parser
parser = argparse.ArgumentParser(description='Process a TSV file.')
parser.add_argument('infile', type=str, help='Path to the input TSV file.')
parser.add_argument('outfile', type=str, help='Path to save the processed output.')
args = parser.parse_args()

# Read the data into a dataframe
df = pd.read_csv(args.infile, sep="\t", header=None, names=["Sample", "Path"])

def get_updated_path(path):
    old_filename = os.path.basename(path).strip()
    new_filename = 'ilmn-' + old_filename
    new_path = os.path.join(os.path.dirname(path), new_filename)
    return new_path
df["Path"] = df["Path"].apply(get_updated_path)

# Write the dataframe to the output file path specified in the arguments
df.to_csv(args.outfile, sep="\t", index=False, header=False)
