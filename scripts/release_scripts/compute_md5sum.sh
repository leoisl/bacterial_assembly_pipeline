#!/bin/bash

# Check if directory path was provided
if [ -z "$1" ]
then
    echo "No directory path provided"
    exit 1
fi

# Define the directory path
directory_path=$1

# Loop through each tar.gz file in the directory structure
find $directory_path -type f -name "*.fa.gz" | while read file
do
  # Compute the md5sum for each file and print it along with the file path
  md5sum "$file"
done

