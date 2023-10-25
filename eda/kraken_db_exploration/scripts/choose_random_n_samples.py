import lzma
from collections import defaultdict
import random
import sys


def pick_random_samples(batches_filename, n):
    batch_to_samples = defaultdict(set)

    with lzma.open(batches_filename, "rt") as fh:
        for line in fh:
            batch_and_order, samples = line.strip().split()
            batch = batch_and_order.split("_")[0]
            samples = set(samples.split(","))

            if batch!="dustbin":
                batch_to_samples[batch].update(samples)

    nb_of_samples_to_pick_from_each_batch = (n // len(batch_to_samples)) + 1

    for batch, samples in batch_to_samples.items():
        print(f"Batch {batch} has {len(samples)} samples, I am picking {nb_of_samples_to_pick_from_each_batch}", file=sys.stderr)
        print("\n".join(random.sample(sorted(samples), nb_of_samples_to_pick_from_each_batch)))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pick random samples from a file.')

    # Add arguments
    parser.add_argument('-n', '--number', type=int, default=1000,
                        help='Number of samples to pick. Default is 1000.')

    parser.add_argument('batches', type=str, help='Path to the batches file.')

    args = parser.parse_args()
    pick_random_samples(args.batches, args.number)


if __name__ == '__main__':
    main()
