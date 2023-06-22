import pandas as pd
import argparse

# set up argument parser
parser = argparse.ArgumentParser(description='Filter 661k samples out of input tsv.')
parser.add_argument('-i', '--input', help='Input TSV file', required=True)
parser.add_argument('-o', '--output', help='Output filtered TSV file', required=True)
args = parser.parse_args()

# read the tsv files into DataFrames
df1 = pd.read_csv(args.input, delimiter='\t')

df2 = pd.read_csv('661k_sample_ids.txt.gz', delimiter='\t', header=None, names=['sample_accession'], compression='gzip')

# only keep rows in df1 where sample_accession is not in df2
df1 = df1[~df1['sample_accession'].isin(df2['sample_accession'])]

# write the filtered DataFrame to the output tsv file
df1.to_csv(args.output, sep='\t', index=False)
