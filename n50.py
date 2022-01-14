from utilities import read_fasta
import re
import argparse


def run(path, N, min_length):
    contigs = read_fasta(path)
    if N == 50:
        N = 0.5
    elif N == 75:
        N = 0.75
    elif N == 25:
        N = 0.25

    length_per_contigs = {}
    total_length = 0
    for i, key in enumerate(contigs.keys()):
        length = re.search(r"length_\d+", key)
        length = length.group()[7:]
        length = int(length)
        if length >= min_length:
            length_per_contigs[i] = length
            total_length += length
        else:
            break

    shortest_length = length
    sum_up = 0
    for node, length in length_per_contigs.items():
        if node == 0:
            longest_length = length
        sum_up += length
        if sum_up >= (total_length * N):
            return node + 1, length, total_length, longest_length, shortest_length


def main():
    parser = argparse.ArgumentParser(
        description="Calculate N from fasta file of SPAdes contigs output"
    )
    parser.add_argument(
        "-in",
        help="fasta input file (required)",
        metavar="",
        dest="input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-N",
        help="Statistics calculation [25, 50, 75] (required)",
        metavar="",
        dest="statistics",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-min",
        help="Cut off the length with specified threshold",
        metavar="",
        dest="min_length",
        type=int,
        default=0,
    )
    args = parser.parse_args()
    n = run(args.input, args.statistics, args.min_length)
    print(f"Number of sequence : {n[0]}")
    print("Your N" + str(args.statistics) + f" length    : {n[1]}")
    print(f"Total length       : {n[2]}")
    print(f"Longest length     : {n[3]}")
    print(f"Shortest length    : {n[4]}")


if __name__ == "__main__":
    main()

