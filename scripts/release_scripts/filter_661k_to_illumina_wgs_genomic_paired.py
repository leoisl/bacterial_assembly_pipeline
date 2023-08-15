import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="This script filters a TSV file and splits a specific column.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path')
parser.add_argument('output_file', metavar='output', type=str, help='the output TSV file path')

# Parse the arguments
args = parser.parse_args()

# Read the TSV file
df = pd.read_csv(args.input_file, delimiter='\t')

# Filter rows to ILLUMINA, WGS, GENOMIC and PAIRED
df = df[(df['instrument_platform'] == 'ILLUMINA') & (df['library_strategy'] == 'WGS') & (df['library_source'] == 'GENOMIC') & (df['library_layout'] == 'PAIRED')]
df.to_csv(args.output_file, sep='\t', index=False)
