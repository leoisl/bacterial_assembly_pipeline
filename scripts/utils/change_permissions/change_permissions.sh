#!/bin/bash

# Check if directory is provided
if [ $# -eq 0 ]
then
    echo "No directory provided. Usage: ./change_permissions.sh /path/to/directory"
    exit 1
fi

# Directory to iterate over, taken from the first argument
dir="$1"

# Iterate over files in the specified directory
find "$dir" -type f -exec chmod 444 {} \;
