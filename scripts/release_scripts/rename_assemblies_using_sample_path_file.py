import os
import argparse


def rename_files(tsv_data):
    updated_tsv = []
    # Skip the header
    for line in tsv_data[1:]:
        sample, path = line.strip().split('\t')
        old_filename = os.path.basename(path).strip()
        new_filename = 'ilmn-' + old_filename
        new_path = os.path.join(os.path.dirname(path), new_filename)

        # Rename the file (uncomment this line when actually renaming files)
        # os.rename(path, new_path)
        print(f"{path} -> {new_path}")

        updated_tsv.append(f'{sample}\t{new_path}')

    return updated_tsv


def main():
    parser = argparse.ArgumentParser(description='Rename files and update TSV.')
    parser.add_argument('input_tsv', type=str, help='Input TSV file path')
    parser.add_argument('output_tsv', type=str, help='Output TSV file path')

    args = parser.parse_args()

    # Read the TSV data from the input file
    with open(args.input_tsv, 'r') as file:
        tsv_data = file.readlines()

    updated_tsv = rename_files(tsv_data)

    # Write the updated TSV to the output file
    with open(args.output_tsv, 'w') as file:
        file.write(tsv_data[0])  # Write the header
        for line in updated_tsv:
            file.write(line + '\n')

    print(f'Updated TSV saved to {args.output_tsv}')


if __name__ == "__main__":
    main()
