# Transform Oilspill FASTA headers to look like FASTQ dito
# Fredrik Boulund 2016


def transform_fasta_header(fastaheader):
    """
    Extract FASTQ filename and read header from Waden Sea FASTA headers.

    FASTA headers look like this:
      BP101_2011-1930_120131_SN1035_0095_BD04PVACXX_s_1_1_sequence_HWI-ST1035_0095_1_1101_17052_27360#ACNGTG/1
    FASTQ headers look like this:
      HWI-ST1035_0095:1:1101:1239:2065#NNNNNN/1
    FASTQ filenames look like this:
      BP101_2011-1930_120131_SN1035_0095_BD04PVACXX_s_1_1_sequence.fastq
      BP101_2011-1930_120131_SN1035_0095_BD04PVACXX_s_1_2_sequence.fastq
    """
    fastq_source, read_header = fastaheader.split("_HWI-", 1)
    rhsplit = read_header.split("_", 1)
    read_header = "HWI-"+rhsplit[0]+"_"+rhsplit[1].translate(str.maketrans("_", ":"))
    fastq_base = fastq_source[:-10]
    return fastq_base, read_header


def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+"1_sequence.fastq", fastq_base+"2_sequence.fastq"

