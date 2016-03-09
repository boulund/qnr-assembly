#!/usr/bin/env python3.5
# Extract sequences matching qnr HMM from FASTQ files
# using headers from FASTA.

from sys import argv, exit, stdout, stderr
from os import listdir, path
from collections import defaultdict
from itertools import chain
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
    parser.add_argument("-q", "--fastq-dir", dest="fastq_dir",
            required=True,
            help="FASTQ directory to read sequences from.")
    parser.add_argument("-1", "--left", dest="left",
            default="",
            help="Destination FASTQ file for 'left' reads [%(default)s].")
    parser.add_argument("-2", "--right", dest="right",
            default="",
            help="Destination FASTQ file for 'right' reads [%(default)s].")
        
    return parser.parse_args()


def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.
    """
    fastq_source, read = fastaheader.split(" ", 1)[0].split("_HWI")
    read_header = "HWI"+read.translate(str.maketrans("_", ":"))
    fastq_base = fastq_source.rsplit("_", 1)[0]
    return fastq_base, read_header
    


def main(options):
    """
    Main function.
    """

    # Construct a dictionary with FASTQ basenames, i.e. not including the pair
    # information (e.g. _1.fasta or _2.fasta) as keys. Values are lists of the first
    # space delimited read headers that should be extracted from the FASTQ files.
    fastq_bases = defaultdict(list)
    for fastafile in options.fasta:
        for header, _ in read_fasta(fastafile):
            fastq_base, read_header = transform_fasta_header(header)
            fastq_bases[fastq_base].append(read_header)
    print("INFO: Number of keys (fastq_basenames) in header dict: {}".format(len(fastq_bases)), file=stderr)
    print("INFO: Number of headers (reads) in dict: {}".format(len(list(chain(*fastq_bases.values())))), file=stderr)
    
    fastq_dir = options.fastq_dir
    fastq_files = set(filename for filename in listdir(options.fastq_dir))

    if options.left and options.right:
        left_fh = open(options.left, 'w')
        right_fh = open(options.right, 'w')
    else:
        left_fh = stdout
        right_fh = stdout
    with left_fh, right_fh:
        for fastq_base, read_headers in fastq_bases.items():
            fastq_left = fastq_base+"_1.fastq"
            fastq_right = fastq_base+"_2.fastq"
            if fastq_left in fastq_files and fastq_right in fastq_files:
                # Iterate both FASTQ files in lock-step, making it 
                # very easy to print out the reads in interleaved order.
                for left, right in zip(read_fastq(path.join(fastq_dir, fastq_left)), 
                                       read_fastq(path.join(fastq_dir, fastq_right))):
                    print(left[0], file=left_fh)
                    print(left[1], file=left_fh)
                    print(left[2], file=left_fh)
                    print(left[3], file=left_fh)
                    print(right[0], file=right_fh)
                    print(right[1], file=right_fh)
                    print(right[2], file=right_fh)
                    print(right[3], file=right_fh)
            else:
                print("WARNING: found no FASTQ files for {}".format(fastq_base), file=stderr)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)

