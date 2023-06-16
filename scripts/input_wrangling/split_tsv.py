import pandas as pd
import argparse
import os

# Initialize the parser
parser = argparse.ArgumentParser(description="This script splits a TSV file into multiple TSV files, each containing n entries.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path')
parser.add_argument('output_dir', metavar='output', type=str, help='the directory to output the split TSV files')
parser.add_argument('n_entries', metavar='n', type=int, help='the number of entries each split TSV file should contain')

# Parse the arguments
args = parser.parse_args()

# Read the TSV file
df = pd.read_csv(args.input_file, delimiter='\t')

# Split dataframe into chunks of size n_entries
chunks = [df[i:i + args.n_entries] for i in range(0, df.shape[0], args.n_entries)]

# Ensure output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# Write each chunk to a new TSV file
for i, chunk in enumerate(chunks):
    output_file = os.path.join(args.output_dir, f'{os.path.basename(args.input_file)}_{i}.tsv')
    chunk.to_csv(output_file, sep='\t', index=False)

