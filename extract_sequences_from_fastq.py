#!/usr/bin/env python3.5
# Extract sequences matching qnr HMM from FASTQ files
# using headers from FASTA.

from sys import argv, exit, stdout, stderr
from os import listdir, path
from collections import defaultdict
from itertools import chain
import importlib
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
            help="Destination FASTQ file for 'left' reads.")
    parser.add_argument("-2", "--right", dest="right",
            default="",
            help="Destination FASTQ file for 'right' reads.")
    parser.add_argument("-t", "--transformer", dest="transformer",
            required=True,
            help="Name of data set header transformer module.")

    if len(argv) < 2:
        parser.print_help()
        exit()
        
    return parser.parse_args()


def main(options):
    """
    Main function.
    """

    # Import fasta header transformer functions
    transformer = importlib.import_module("transformers."+options.transformer)
    transform_fasta_header = transformer.transform_fasta_header
    fastq_filename = transformer.fastq_filename

    # Construct a dictionary with FASTQ basenames, i.e. not including the pair
    # information (e.g. _1.fasta or _2.fasta) as keys. Values are lists of the first
    # space delimited read headers that should be extracted from the FASTQ files.
    fastq_bases = defaultdict(list)
    for fastafile in options.fasta:
        try:
            for header, _ in read_fasta(fastafile):
                fastq_base, read_header = transform_fasta_header(header)
                fastq_bases[fastq_base].append(read_header)
        except IOError:
            print("WARNING: Could not parse {}".format(fastafile)) 
            continue
    print("INFO: Number of keys (fastq_basenames) in header dict: {}".format(len(fastq_bases)), file=stderr)
    print("INFO: Number of headers (reads) in dict: {}".format(len(list(chain(*fastq_bases.values())))), file=stderr)
    
    fastq_dir = options.fastq_dir
    fastq_files = set(filename for filename in listdir(options.fastq_dir))

    warnings_occurred = False
    if options.left and options.right:
        left_fh = open(options.left, 'w')
        right_fh = open(options.right, 'w')
    else:
        left_fh = stdout
        right_fh = stdout
    with left_fh, right_fh:
        for fastq_base, read_headers in fastq_bases.items():
            header_set = set(read_headers)
            fastq_left, fastq_right = fastq_filename(fastq_base)
            if fastq_left in fastq_files and fastq_right in fastq_files:
                # Iterate both FASTQ files in lock-step, making it 
                # very easy to print out the reads in interleaved order.
                for left, right in zip(read_fastq(path.join(fastq_dir, fastq_left)), 
                                       read_fastq(path.join(fastq_dir, fastq_right))):
                    left_header = left[0][1:].split(" ", 1)[0]
                    right_header = right[0][1:].split(" ", 1)[0]
                    if left_header in header_set or right_header in header_set:
                        print(left[0], file=left_fh)
                        print(left[1], file=left_fh)
                        print(left[2], file=left_fh)
                        print(left[3], file=left_fh)
                        print(right[0], file=right_fh)
                        print(right[1], file=right_fh)
                        print(right[2], file=right_fh)
                        print(right[3], file=right_fh)
            else:
                print("WARNING: found no FASTQ files for {} and {}".format(fastq_left, fastq_right), file=stderr)
                warnings_occurred = True
    if warnings_occurred:
        print("WARNING: Possible reasons for warnings include:\n"
              "  - selecting the wrong transformer\n"
              "  - including incorrect FASTQ files", file=stderr)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)

