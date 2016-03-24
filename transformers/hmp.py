# Transform HMP fasta headers to FASTQ dito
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like a lot of things (most importantly, all ':' have been replaced by '_'):
      SRS078176.denovo_duplicates_marked.trimmed.2_HWI-6X_10148_FC61V2D_4_111_8296_18840/2
    FASTQ headers look like a lot of things:
      61NNNAAXX100509:5:100:10000:16724/2
      HWI-EAS97_103024977:5:100:10000:19481/2
      HWI-ST115_0123:8:100:10022:9867/1
      HWUSI-EAS776_102431267:1:100:10006:2180/2
      USI-EAS034_0002:1:100:10002:6226/1
      ILLUMINA-0648E5_0001:1:100:10001:15283/1
      SOLEXA3_0013:2:100:10001:18706/1
      SRR061245.1000/1
    FASTQ filenames look like:
      SRS078176.denovo_duplicates_marked.trimmed.1.fastq
    """
    translator = str.maketrans("_", ":")
    fastq_source, read = fastaheader.split(" ", 1)[0].split("trimmed.")
    read_header = read[2:]  
    if read_header.startswith("6"):
        read_header = read_header.translate(translator)
    elif read_header.startswith(("HW", "ILLUMINA", "USI", "SOL")):
        read_header = read_header[:read_header.find("_")] + "_" + read_header[read_header.find("_")+1:].translate(translator)
    fastq_base = fastq_source+"trimmed"
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+".1.fastq", fastq_base+".2.fastq"

