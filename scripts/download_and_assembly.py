import pandas as pd
import requests
import hashlib
import argparse
import os
import subprocess
import logging
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the parser
parser = argparse.ArgumentParser(description="This script downloads files from provided URLs, checks their integrity with MD5 hashes, and then assembles them with Shovill.")

# Add the arguments
parser.add_argument('input_file', metavar='input', type=str, help='the input TSV file path')
parser.add_argument('output', metavar='output', type=str, help='the output directory path')
parser.add_argument('metadata', metavar='metadata', type=str, help='the metadata tsv file')
parser.add_argument('timeout', metavar='timeout', type=int, help='Timeout in seconds')
parser.add_argument('fast_dir', metavar='fast_dir', type=str, help='Fast temp dir (e.g. /tmp, /scratch, etc...)')
parser.add_argument('--skip-assembly', dest='skip_assembly', action='store_true', help='Skip assembly and only download files')
parser.add_argument('--keep-reads', dest='keep_reads', action='store_true', help='Keep reads')

# Parse the arguments
args = parser.parse_args()

def download_file_using_ftp(url, filename):
    url = f"https://{url}"
    logging.info(f"Downloading {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we got an OK response

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def download_file_using_fire(url, filename):
    s3_url = url.replace("ftp.sra.ebi.ac.uk/vol1/", "s3://era-public/")
    logging.info(f"Downloading {s3_url}")
    s3_command = ["aws", "--no-sign-request", "--endpoint-url", "https://hl.fire.sdo.ebi.ac.uk", "s3", "cp", s3_url , filename]
    logging.info(f"Running {' '.join(s3_command)}")
    subprocess.run(s3_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


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

with open(args.metadata, "w") as metadata_fh, \
    tempfile.TemporaryDirectory(prefix="deleteme_", dir=args.fast_dir) as tempdir:
    os.environ['TMPDIR'] = str(tempdir)
    for _, row in df.iterrows():
        accession = row['sample_accession']

        temp_outdir = os.path.join(tempdir, accession)
        os.makedirs(temp_outdir, exist_ok=True)
        reads_dir = temp_outdir if args.keep_reads else tempdir

        filenames = []
        try:
            for i in range(1, 3):  # For both files R1 and R2
                url = row['fastq_ftp_R' + str(i)]
                md5_expected = row['fastq_md5_R' + str(i)]

                filename = os.path.join(reads_dir, os.path.basename(url))

                # Download the file
                download_file_using_fire(url, filename)

                # Compute the file's MD5 hash and compare it with the expected value
                md5_actual = compute_md5(filename)

                if md5_actual != md5_expected:
                    raise ValueError(f"MD5_check_failed : File {filename} MD5 check failed. Expected {md5_expected}, got {md5_actual}")
                else:
                    logging.info(f"File {filename} downloaded and MD5 check passed.")

                filenames.append(filename)

            # Assemble the reads with Shovill
            if not args.skip_assembly:
                shovill_command = ['shovill', '--R1', filenames[0], '--R2', filenames[1], '--outdir', temp_outdir, '--cpus', '1', '--force']
                logging.info(f"Running {' '.join(shovill_command)}")
                subprocess.run(shovill_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=args.timeout)


            # copy temp_outdir to outdir
            outdir = os.path.join(args.output, accession)
            shutil.copytree(temp_outdir, outdir)

            logging.info(f"[SAMPLE_REPORT] SUCCESS {accession}")
            print(f"{accession}\tSUCCESS", file=metadata_fh)
        except Exception as e:
            logging.info(f"[SAMPLE_REPORT] ERROR {accession}")
            logging.error("An error occurred: %s", str(e))
            print(f"{accession}\tERROR\t{e}", file=metadata_fh)
        finally:
            if not args.keep_reads:
                # Delete the input files
                for filename in filenames:
                    # Check if the file exists
                    if os.path.exists(filename):
                        # If it does, remove it
                        logging.info(f"Deleting {filename}")
                        os.remove(filename)
