import pandas as pd
import requests
import hashlib
import argparse
import os
import subprocess

# Initialize the parser
parser = argparse.ArgumentParser(description="This script downloads files from provided URLs, checks their integrity with MD5 hashes, and then assembles them with Shovill.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path')
parser.add_argument('output', metavar='output', type=str, help='the output directory path')

# Parse the arguments
args = parser.parse_args()

def download_file(url, filename):
    response = requests.get(f"https://{url}", stream=True)
    response.raise_for_status()  # Ensure we got an OK response

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def compute_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Read the TSV file
df = pd.read_csv(args.input_file, delimiter='\t')

# Create the output directory if it doesn't exist
os.makedirs(args.output, exist_ok=True)

for _, row in df.iterrows():
    filenames = []
    for i in range(1, 3):  # For both files R1 and R2
        url = row['fastq_ftp_R' + str(i)]
        md5_expected = row['fastq_md5_R' + str(i)]

        filename = os.path.join(args.output, os.path.basename(url))

        # Download the file
        download_file(url, filename)

        # Compute the file's MD5 hash and compare it with the expected value
        md5_actual = compute_md5(filename)

        if md5_actual != md5_expected:
            raise ValueError(f"File {filename} MD5 check failed. Expected {md5_expected}, got {md5_actual}")
        else:
            print(f"File {filename} downloaded and MD5 check passed.")

        filenames.append(filename)

    # Make output directory within the specified output directory
    outdir = os.path.join(args.output, row['run_accession'])
    os.makedirs(outdir, exist_ok=True)

    # Assemble the reads with Shovill
    subprocess.run(['shovill', '--R1', filenames[0], '--R2', filenames[1], '--outdir', outdir, '--cpus', '1'], check=True)

    # Delete the input files
    for filename in filenames:
        os.remove(filename)
