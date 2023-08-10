import pandas as pd
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="This script filters a TSV file and splits a specific column.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path')
parser.add_argument('output_file', metavar='output', type=str, help='the output TSV file path')
parser.add_argument('error_file', metavar='error', type=str, help='the error TSV file path')

# Parse the arguments
args = parser.parse_args()

# Read the TSV file
df = pd.read_csv(args.input_file, delimiter='\t')

# Move 'sample_accession' to the first column
column_list = df.columns.tolist()
column_list.insert(0, column_list.pop(column_list.index('sample_accession')))
df = df.reindex(columns=column_list)

# Filter rows to ILLUMINA, WGS, GENOMIC and PAIRED
df = df[(df['instrument_platform'] == 'ILLUMINA') & (df['library_strategy'] == 'WGS') & (df['library_source'] == 'GENOMIC') & (df['library_layout'] == 'PAIRED')]
df.to_csv(args.output_file+".illumina_wgs_genomic_paired.csv", sep='\t', index=False)

# Output samples with multiple runs
multiple_runs_df = df[df.duplicated(subset='sample_accession')]
multiple_runs_df.to_csv(args.output_file+".multiple_runs.csv", sep='\t', index=False)

# Keep only desired columns
df = df[['sample_accession', 'run_accession', 'fastq_ftp', 'fastq_md5', 'read_count', 'base_count']]

# Keep only samples with a single run
df = df[~df.duplicated(subset='sample_accession') & ~df.duplicated(subset='sample_accession', keep='last')]

# remove rows where read_count is less than 1000
df['read_count'] = pd.to_numeric(df['read_count'], errors='coerce')
df = df[df['read_count'] >= 1000]

# remove rows where 'sample_accession' contains ";"
df = df[~df['sample_accession'].str.contains(";")]

# Split fastq_ftp column and expand into new dataframe
split_df = df['fastq_ftp'].str.split(';', expand=True)

# Create error dataframe
error_df = df[split_df.iloc[:, :2].isna().any(axis=1) | ~split_df.iloc[:, 2:].isna().all(axis=1)]
error_df.to_csv(args.error_file, sep='\t', index=False)

# Filter df for rows that are not in error_df
df = df[~df['run_accession'].isin(error_df['run_accession'])]

# Add split columns back to the original dataframe
df[['fastq_ftp_R1', 'fastq_ftp_R2']] = split_df.loc[df.index, :].iloc[:, 0:2]

# Split fastq_md5 column and expand into new dataframe
split_md5_df = df['fastq_md5'].str.split(';', expand=True)
df[['fastq_md5_R1', 'fastq_md5_R2']] = split_md5_df.loc[df.index, :].iloc[:, 0:2]

# Remove the original 'fastq_ftp' and 'fastq_md5' columns
df = df.drop(columns=['fastq_ftp', 'fastq_md5'])

# Cast read_count and base_count to int
df['read_count'] = df['read_count'].astype(int)
df['base_count'] = df['base_count'].astype(int)

# Write the result back to a new TSV file
df.to_csv(args.output_file, sep='\t', index=False)

