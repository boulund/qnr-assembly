# Transform Waden Sea FASTA headers
# Fredrik Boulund 2016


def transform_fasta_header(fastaheader):
    """
    Extract FASTQ filename and read header from Waden Sea FASTA headers.

    FASTA headers look like this:
      >SRR490742_1_SRR490742.40459 ISGA2X_0003_FC636NY_3_2_17267_19208 length=161
    FASTQ headers look like this:
      @SRR490742.1 ISGA2X_0003_FC636NY:3:1:4899:1009 length=161
    FASTQ filenames look like this:
      SRR490742_1.fastq
    """

    fastq_source, read_header = fastaheader.split(" ", 1)[0].rsplit("_", 1)
    fastq_base = fastq_source.rsplit("_", 1)[0][:-2]
    return fastq_base, read_header


