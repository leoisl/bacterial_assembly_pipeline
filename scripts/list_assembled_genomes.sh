#!/bin/bash

# Check if a directory has been provided
if [ $# -eq 0 ]; then
    echo "No directory supplied. Usage: ./script.sh /path/to/tar/files"
    exit 1
fi

# Directory to search for tar.gz files
dir=$1

for file in "$dir"/*.tar.gz
do
    tar -tf $file | grep 'contigs.fa'
done

