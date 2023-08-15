import argparse
import pandas as pd

# Define the CLI argument parser
parser = argparse.ArgumentParser(description='Process a TSV file.')
parser.add_argument('infile', type=str, help='Path to the input TSV file.')
parser.add_argument('outfile', type=str, help='Path to save the processed output.')
args = parser.parse_args()

# Read the data into a dataframe
df = pd.read_csv(args.infile, sep="\t", header=None)

df[1] = df[1].apply(lambda x: "ilmn-" + x)

# Write the dataframe to the output file path specified in the arguments
df.to_csv(args.outfile, sep="\t", index=False, header=False)
