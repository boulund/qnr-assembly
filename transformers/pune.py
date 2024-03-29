# Transform pune headers
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.
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

