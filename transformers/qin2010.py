# Transform qin 2010 headers
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.
    """
    fastq_base = fastaheader[:fastaheader.find(".raw.")+4]
    read_header = fastaheader[fastaheader.find(".raw.")+7:]
    read_header = read_header[::-1].replace("_", ":", 3)[::-1]
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+".1.fq", fastq_base+".2.fq"


