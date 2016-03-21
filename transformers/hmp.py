# Transform HMP fasta headers to FASTQ dito
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like:
      SRS078176.denovo_duplicates_marked.trimmed.2_HWI-6X_10148_FC61V2D_4_111_8296_18840/2
    FASTQ headers look like:
      HWI-6X_10148_FC61V2D_4_100_10000_14055/1
    FASTQ filenames look like:
      SRS078176.denovo_duplicates_marked.trimmed.1.fastq
    """
    fastq_source, read = fastaheader.split(" ", 1)[0].split("_HWI")
    read_header = "HWI-"+read
    fastq_base = fastq_source.rsplit(".", 1)[0]
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+".1.fastq", fastq_base+".2.fastq"
