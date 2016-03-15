# Transform qin 2012 headers
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like:
      DLM002_SRR341590.925753_FC61AVBAAXX_5_31_7577_16250_length=148
    FASTQ headers look like:
      SRR341608.1 FC61AVBAAXX:2:1:999:16572 length=148
    FASTQ filenames look like:
      DOM012.fastq
    """
    fastq_base, read_header, _ = fastaheader.split("_", 2)
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+".fastq", fastq_base+".fastq"


