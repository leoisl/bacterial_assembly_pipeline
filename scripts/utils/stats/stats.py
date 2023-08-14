import pandas as pd
import argparse

columns = ["library_selection", "last_updated", "instrument_platform", "instrument_model",
           "library_strategy", "library_source", "library_layout", "center_name", "first_created", "scientific_name", "tax_id"]

# Initialize the parser
parser = argparse.ArgumentParser(description="This creates several stats based on certain columns of the ENA metadata file.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path (ENA metadata file)')

# Parse the arguments
args = parser.parse_args()

# Read the TSV file
df = pd.read_csv(args.input_file, delimiter='\t')
df["last_updated"] = df["last_updated"].apply(lambda x: str(x).split("-")[0])
df["first_created"] = df["first_created"].apply(lambda x: str(x).split("-")[0])

# Print stats
pd.set_option('display.max_rows', None)
for column in columns:
    print(f"Stats for column {column}")
    # Filter out counts with value 1
    value_counts = df[column].value_counts()
    value_counts_filtered = value_counts[value_counts > 1]
    print(value_counts_filtered)
    print()
