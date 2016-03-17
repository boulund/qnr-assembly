# Transform PETL fasta headers to FASTQ dito
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like:
      >8_111221_AC03V3ACXX_JL34_index11_1_HWI-ST1018_8_1102_13436_5796#0/1
    FASTQ headers look like:
      @HWI-ST1018:1:1101:4680:2245#0/1
    FASTQ filenames look like:
      1_120228_AD0J14ACXX_JL19_index7_1.fastq
    """
    fastq_source, read = fastaheader.split(" ", 1)[0].split("_HWI")
    read_header = "HWI"+read.translate(str.maketrans("_", ":"))
    fastq_base = fastq_source.rsplit("_", 1)[0]
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+"_1.fastq", fastq_base+"_2.fastq"

