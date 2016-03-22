# Transform Tara ocean fasta headers to FASTQ dito
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like:
      ERR598954_1_ERR598954.1005434 H3_D1BKNACXX_8_1101_14029_60161/1
    FASTQ headers look like:
      ERR598954.1 H3:D1BKNACXX:8:1101:1348:2102/1
    FASTQ filenames look like:
      ERR598954_1.fastq
      ERR598954_2.fastq
    """
    fastq_source, read_header = fastaheader.split(" ", 1)[0].rsplit("_", 1)
    fastq_base = fastq_source.split("_", 1)[0]
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+"_1.fastq", fastq_base+"_2.fastq"

