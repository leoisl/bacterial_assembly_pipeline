import pandas as pd
import argparse

def concatenate_tsvs(tsv1_path, tsv2_path, output_path):
    # Load the TSV files into pandas dataframes
    df1 = pd.read_csv(tsv1_path, sep='\t', dtype=str)
    df2 = pd.read_csv(tsv2_path, sep='\t', dtype=str)

    # Rename the column 'sample_id' in the second dataframe to 'sample_accession'
    df2.rename(columns={'sample_id': 'sample_accession'}, inplace=True)

    # Concatenate the records of both dataframes based on common columns
    concatenated_df = pd.concat([df1, df2], join='inner', ignore_index=True)

    # Save the concatenated dataframe to the specified output path
    concatenated_df.to_csv(output_path, sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate two TSVs based on common columns.")
    parser.add_argument("tsv1_path", help="Path to the 1300k TSV file")
    parser.add_argument("tsv2_path", help="Path to the 661k TSV file")
    parser.add_argument("output_path", help="Path to save the concatenated TSV")

    args = parser.parse_args()

    concatenate_tsvs(args.tsv1_path, args.tsv2_path, args.output_path)
