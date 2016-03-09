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
