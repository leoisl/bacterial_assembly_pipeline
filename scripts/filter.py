import pandas as pd

# Read the TSV file into a DataFrame.
df = pd.read_csv('all_bacteria_data.tsv', delimiter='\t')

# Filter rows where column1 equals 'value1' and column2 equals 'value2'.
filtered_df = df[(df['instrument_platform'] == 'ILLUMINA') & (df['library_strategy'] == 'WGS') & (df['library_source'] == 'GENOMIC') & (df['library_layout'] == 'PAIRED')]

# If you want to write the filtered data to a new TSV file, you can do so with the to_csv function.
filtered_df.to_csv('all_bacteria_data.filtered.tsv', sep='\t', index=False)
