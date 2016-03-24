#!/usr/bin/env python3.5
# Fredrik Boulund 2016
# Extract sub sequences from a FASTA file using ranges
# added to FASTA headers by Easel bash pipeline.

from read_fasta import read_fasta
from sys import argv, exit, stdout
from collections import namedtuple, OrderedDict
import argparse


def parse_args(argv):
    """
    Parse commandline arguments.
    """

    desc = """Extract sub sequences from FASTA files. Fredrik Boulund 2016"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("PFA",
            help="Protein FASTA file(s) to read headers with range information from.")
    parser.add_argument("NFA",
            help="Nucleotide FASTA file(s) to read sub sequences from.")
    parser.add_argument("-p", "--prefix", 
            help="FASTA header prefix to replace previous header with.")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILE instead of STDOUT.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def extract_subsequence_records(fastafile):
    """
    Extract sub sequence records (reading frame and start, end) from FASTA headers.

    The following format of headers is expected:
      >NODE_60_length_635_cov_2.53448_ID_19982_5/10-212
                                               ^ ^  ^
                                               | |  End
                                               | Start
                                               Reading frame
    The start and end in the header are 1-based in protein sequence coordinates.
    The function returns the equivalent 0-based nucleotide sequence coordinates.
    """

    Subsequence_Record = namedtuple("Subsequence_Record", "frame, start, end")
    subsequence_records = OrderedDict()
    for long_header, sequence in read_fasta(fastafile, keep_formatting=False):
        header, frame_start_end = long_header.rsplit("_", 1)
        frame, start_end = frame_start_end.split("/")
        start, end = start_end.split("-")
        subseq_rec = Subsequence_Record(int(frame), int(start)*3-3, int(end)*3-3)
        subsequence_records[header] = subseq_rec
    return subsequence_records


def revcomp(sequence):
    """
    Return the reverse complement of DNA sequence.
    """
    return sequence.upper().translate(str.maketrans("ACGT", "TGCA"))[::-1]


def extract_subseq(sequence, subseq): #frame, start, end):
    """
    Extract subsequence from a sequence string.

    This follows EMBOSS transeq's implementation on how
    reading frames are interpreted. The starting position
    of the reverse complement is adjusted based on the 
    total length of the sequence modulo 3, so that the
    reverse frames correspond to the same position of the 
    frames in the forward sequence.
    """
    reverse_adjustment = len(sequence) % 3
    if subseq.frame == 1:
        return sequence[subseq.start:subseq.end]
    elif subseq.frame == 2:
        return sequence[1:][subseq.start:subseq.end]
    elif subseq.frame == 3:
        return sequence[2:][subseq.start:subseq.end]
    elif subseq.frame == 4:
        start = subseq.start + reverse_adjustment
        end = subseq.end + reverse_adjustment
        return revcomp(sequence)[start:end]
    elif subseq.frame == 5:
        start = subseq.start + reverse_adjustment
        end = subseq.end + reverse_adjustment
        return revcomp(sequence)[2:][start:end]
    elif subseq.frame == 6:
        start = subseq.start + reverse_adjustment
        end = subseq.end + reverse_adjustment
        return revcomp(sequence)[1:][start:end]


def main(options):
    """
    Main function
    """

    subsequences = extract_subsequence_records(options.PFA)
    nucleotide_sequences = {h: s for h, s in read_fasta(options.NFA, keep_formatting=False)}

    if options.outfile:
        outfile = open(options.outfile, 'w')
    else:
        outfile = stdout

    with outfile:
        for counter, header_subseq in enumerate(subsequences.items(), start=1):
            header, subseq = header_subseq
            if options.prefix:
                print(">"+options.prefix+"_"+str(counter), header, subseq, file=outfile)
            else:
                print(">"+header, subseq, file=outfile)
            e_subseq = extract_subseq(nucleotide_sequences[header], subseq) 
            print(e_subseq, file=outfile)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)
