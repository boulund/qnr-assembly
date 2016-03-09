#!/usr/bin/env python3.5
# Extract sequences matching qnr HMM from FASTQ files
# using headers from FASTA.

from sys import argv, exit
import argparse

from read_fasta import read_fasta, read_fastq

def parse_args(argv):
    """
    Parse command line
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--fasta", nargs="+", dest="fasta",
            required=True,
            help="FASTA file(s) to read headers from.")
    parser.add_argument("-q", "--fastq", nargs="+", dest="fastq",
            required=True,
            help="FASTQ file(s) to read headers from.")
        
    return parser.parse_args()


def transform_fasta_header(header):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.
    """
    return "HWI"+header.split(" ", 1)[0].split("_HWI")[1].translate(str.maketrans("_", ":"))


def main(options):
    """
    Main function.
    """

    fasta_headers = set()
    headeradd = fasta_headers.add
    for fastafile in options.fasta:
        for header, _ in read_fasta(fastafile):
            headeradd(transform_fasta_header(header))
    for fastqfile in options.fastq:
        for header, seq, second_header, scores in read_fastq(fastqfile):
            clean_header = header[1:].split(" ", 1)[0]
            if clean_header in fasta_headers:
                print(header)
                print(seq)
                print(second_header)
                print(scores)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)

