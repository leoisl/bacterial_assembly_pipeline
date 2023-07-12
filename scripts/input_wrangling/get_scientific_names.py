import pandas as pd

# Load the TSV file
df = pd.read_csv("all_bacteria_data.tsv", sep="\t", usecols=['scientific_name'], dtype={'scientific_name': str})

# Define a function to extract the first two words of a string
def get_first_two_words(s):
    words = str(s).split()
    return " ".join(words[:2])

# Apply the function to the 'scientific_name' column
df['scientific_name'] = df['scientific_name'].apply(get_first_two_words)

# Count the frequency of each scientific name
scientific_name_counts = df['scientific_name'].value_counts()

# Convert to DataFrame
scientific_name_counts_df = scientific_name_counts.reset_index()
scientific_name_counts_df.columns = ['scientific_name', 'count']

# Sort by count, larger first
scientific_name_counts_df = scientific_name_counts_df.sort_values(by='count', ascending=False)

scientific_name_counts_df.to_csv("scientif_names_stats.tsv", sep="\t", index=False)
