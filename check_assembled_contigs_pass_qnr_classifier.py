#!/usr/bin/env python3.5
# Fredrik Boulund 2016
# Extract sequences from a FASTA file 

from read_fasta import read_fasta
from sys import argv, exit, maxsize
from subprocess import Popen, PIPE
import shlex
import argparse


def parse_args(argv):
    """
    Parse commandline arguments.
    """

    desc = """Run hmmsearch and report sequences passing qnr classifier. Fredrik Boulund 2016"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("DOMTBL", 
            help="hmmsearch domtblout file to parse.")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILE instead of STDOUT.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def parse_domtbl(filename, min_score=0):
    '''
    Parses hmmsearch domain table output (--domtblout)

    Returns target name, tlen, domain score.
    '''

    with open(filename) as f:
        for line in f:
            if line.startswith("#"):
                continue
            domtbl_line = line.split()
            target_name = domtbl_line[0]
            tlen = int(domtbl_line[2])
            domain_score = float(domtbl_line[7])
            yield (target_name, tlen, domain_score)


def classify_qnr(sequence_length, domain_score, func="", longseqcutoff=75, longseqdef=85, minlength=20):
    """
    Classifies a sequence as Qnr or not.

    Uses the domain_score and a user defined function
    to classify a given sequence as putative Qnr or not.
    Contains a hardcoded minimum fragment length of 10 
    under which the function will unconditionally return false.

    Input::

        sequence_length an integer with the sequence length.
        domain_score    a float with the domain score for this sequence.
        func            an optional function to determine classification.
        longseqcutoff   the classification cutoff (minimum score) for long qnr 
                        sequences.
        longseqdef      the definition for long sequences.
        minlength       minimum fragment length allowed.

    Returns::

        classification  a boolean determining whether it should be classified
                        as Qnr or not.

    Errors::

        (none)
    """
    
    # Define a hardcoded function if none given
    if func == "":
        k = 0.7778
        m = -7.954
        func = lambda L: k*L + m
    
    # Pretty self-explanatory. Has a range in which the classification
    # function is used, determined by the first if-statement 
    if (int(sequence_length) >= int(longseqdef)) and (float(domain_score) >= float(longseqcutoff)):
        return True
    elif int(sequence_length) < minlength: # PREVOUSLY HARDCODED MIN FRAGMENT LENGTH 20
        return False
    elif int(sequence_length) < int(longseqdef):
        if float(domain_score) > func(float(sequence_length)):
            return True
        else:
            return False
    else:
        return False


def main():
    """
    Main function.
    """
    options = parse_args(argv)

    for target, tlen, domain_score  in parse_domtbl(options.DOMTBL):
        if classify_qnr(tlen, domain_score):
            print("Qnr: {}".format(target))
        else:
            print("NOT qnr: {}".format(target))


if __name__ == "__main__":
    main()

