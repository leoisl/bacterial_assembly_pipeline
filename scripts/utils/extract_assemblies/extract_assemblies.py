from pathlib import Path
import tarfile
import gzip
import hashlib
import logging
import sys
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)

def extract_and_gzip(file_path, output_path):
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            if member.name.endswith('contigs.fa'):
                prefix = Path(member.name).parent.name # Get the parent directory name
                new_filename = f"{prefix}_{Path(member.name).name}.gz"
                file = tar.extractfile(member)
                if file:  # if the file object is not None
                    md5_file = md5_in_memory_file(file)

                    gzip_file = output_path / new_filename
                    with gzip.open(gzip_file, 'wb') as f_out:
                        f_out.writelines(file)  # write content of .fa file to .gz file

                    md5_gzip_file = md5_of_uncompressed_file(gzip_file)

                    if md5_file != md5_gzip_file:
                        logging.warning(f"MD5 mismatch for {member.name}({md5_file}) and {gzip_file}({md5_gzip_file})")
                        gzip_file.unlink()
                    else:
                        logging.info(f"Extracted {member.name} to {gzip_file} successfully")
                else:
                    logging.warning(f"Could not extract {member.name}")


def md5_in_memory_file(file_obj):
    file_obj.seek(0)  # make sure we are at the beginning of the file
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_obj.read(4096), b""):
        hash_md5.update(chunk)
    file_obj.seek(0)  # restart file pointer to beginning of file
    return hash_md5.hexdigest()


def md5_of_uncompressed_file(fname):
    hash_md5 = hashlib.md5()
    with gzip.open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract assembly files and gzips them")

    parser.add_argument('-i', '--input_file', required=True, help="Path to a .txt file containing paths to .tar.gz files to process")
    parser.add_argument('-o', '--output_dir', required=True, help="Path to the output directory")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        tar_files = [line.strip() for line in f]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


    for file_path in tar_files:
        extract_and_gzip(file_path, output_dir)


if __name__ == "__main__":
    main()
