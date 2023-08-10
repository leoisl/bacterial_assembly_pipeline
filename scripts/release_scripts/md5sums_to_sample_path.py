import sys
from pathlib import Path

print("Sample\tPath")  # Print the header
for line in sys.stdin:
    _, path_str = line.strip().split()  # Split the line into hash and path
    path = Path(path_str)
    sample = path.stem.split('_')[0]  # Extract the sample from the filename (stem)
    print(f"{sample}\t{path}")  # Print the sample and path

