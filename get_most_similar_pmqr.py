#!/usr/bin/env python3.5
# Get most similar plasmid mediated qnr using Clustal Omega distmatrix output.
# Fredrik Boulund 2016

from sys import argv, exit, stdout, stderr
from os import listdir, path
from itertools import chain
from collections import OrderedDict
from operator import itemgetter
import argparse

def parse_args(argv):
    """
    Parse command line
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("DISTMAT",
            help="Distance matrix file")
    parser.add_argument("-n", dest="n", metavar="N",
            type=int,
            default=0,
            help="Print the N most similar sequences instead of printing table of only the single most similar sequence.")


    if len(argv) < 2:
        parser.print_help()
        exit()
        
    return parser.parse_args()


def parse_distmatrix(filename):
    """
    Parse Clustal Omega distance matrix output.
    Assumes --percent-id was enabled during creation.
    """

    distmat = OrderedDict()
    with open(filename) as f:
        line = f.readline()  # Skip the first line containing number of sequences in alignment
        for line in f:
            row = line.split()
            distmat[row[0]] = row[1:]
    return distmat



def main(options):
    """
    Main function.
    """

    distmat = parse_distmatrix(options.DISTMAT)
    contigs = list(distmat.keys())
    if not options.n:
        print("{:<54} {:<54} {:>5}".format("Contig", "MostSim", "% ID"))
    for pos, seqinfo in enumerate(distmat.items()):
        if not seqinfo[0].startswith("Qnr"):
            most_similar_sorted = sorted(enumerate(map(float, (seqinfo[1]))), key=itemgetter(1), reverse=True)
            contig = contigs[pos]
            if options.n:
                print(contig)
                most_similar = []
                for ms, pid in most_similar_sorted[1:options.n+1]:
                    most_similar.append(pid)
                    most_similar.append(contigs[ms])
                format_string = "  {:>5.2f} {}\n"*options.n
                print(format_string.format(*most_similar))
            else:
                most_similar = contigs[most_similar_sorted[1][0]]
                pid = most_similar_sorted[1][1]
                print("{:<54} {:<54} {:>5.2f}".format(contig, most_similar, pid))

    


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)

