import pandas as pd
import argparse

def process_data(tsv1_path, tsv2_path, output_path):
    # Load the TSV files into pandas DataFrames
    df1 = pd.read_csv(tsv1_path, sep='\t')
    df2 = pd.read_csv(tsv2_path, sep='\t')

    # Filter rows to ILLUMINA, WGS, GENOMIC and PAIRED
    df1_filtered = df1[(df1['instrument_platform'] == 'ILLUMINA') & (df1['library_strategy'] == 'WGS') & (df1['library_source'] == 'GENOMIC') & (df1['library_layout'] == 'PAIRED')]

    # Filter rows from the first dataframe where the sample_accession is in the second dataframe
    df1_filtered = df1_filtered[df1_filtered['sample_accession'].isin(df2['Sample'])]

    # Move 'sample_accession' to the first column
    column_list = df1_filtered.columns.tolist()
    column_list.insert(0, column_list.pop(column_list.index('sample_accession')))
    df1_filtered = df1_filtered.reindex(columns= column_list)

    # Save the filtered DataFrame to a TSV file
    df1_filtered.to_csv(output_path, sep='\t', index=False)

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Process two TSV files and output a filtered TSV file.')
    parser.add_argument('tsv1_path', help='Path to all_bacteria_data.tsv.')
    parser.add_argument('tsv2_path', help='Path to sample_path.tsv.')
    parser.add_argument('output_path', help='Path to save the output TSV file.')

    # Parse arguments
    args = parser.parse_args()

    # Process data
    process_data(args.tsv1_path, args.tsv2_path, args.output_path)

if __name__ == '__main__':
    main()

