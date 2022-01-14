from ast import arg
from os import path
from traceback import print_tb
from utilities import read_fasta
import re
import argparse


def run(path, NG, genome_length):
    contigs = read_fasta(path)
    if NG == 50:
        NG = 0.5
    elif NG == 75:
        NG = 0.75
    elif NG == 25:
        NG = 0.25

    length_per_contigs = {}
    for i, key in enumerate(contigs.keys()):
        length = re.search(r"length_\d+", key)
        length = length.group()[7:]
        length = int(length)
        length_per_contigs[i] = length

    shortest_length = length
    sum_up = 0
    for node, length in length_per_contigs.items():
        if node == 0:
            longest_length = length
        sum_up += length
        if sum_up >= (genome_length * NG):
            return node + 1, length, genome_length, longest_length, shortest_length


def main():
    parser = argparse.ArgumentParser(
        description="Calculate NG from fasta file of SPAdes contigs output"
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
        help="Statistics calculation (required)",
        metavar="",
        dest="statistics",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-L",
        help="Length of the reference genome (required)",
        dest="length",
        metavar="",
        type=int,
        required="TRUE",
    )
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ng = run(args.input, args.statistics, args.length)
    print(f"Number of sequence : {ng[0]}")
    print("Your NG" + str(args.statistics) + f" length   : {ng[1]}")
    print(f"Genome length      : {ng[2]}")
    print(f"Longest length     : {ng[3]}")
    print(f"Shortest length    : {ng[4]}")


if __name__ == "__main__":
    main()
