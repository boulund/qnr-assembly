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
    
    fastq_basenames = {
        "DLM002": "SRR341590",
        "DLM003": "SRR341591",
        "DLM004": "SRR341592",
        "DLM005": "SRR341593",
        "DLM007": "SRR341595",
        "DLM008": "SRR341596",
        "DLM011": "SRR341598",
        "DOM005": "SRR341607",
        "DOM012": "SRR341608",
        "DOM017": "SRR341610",
        "DOM020": "SRR341611",
        "DOM023": "SRR341613",
        "DOM024": "SRR341614",
        "DOM025": "SRR341615",
        "NLM001": "SRR341625",
        "NLM005": "SRR341627",
        "NOM008": "SRR341646",
        "NOM013": "SRR341648",
        "NOM026": "SRR341652",
        "DLM014": "SRR341662",
        "NLM021": "SRR341699",
        "NLM022": "SRR341700",
        "NLM026": "SRR341702",
        "NLM029": "SRR341705",
        "NLM031": "SRR341706",
        "NLM032": "SRR341707",
        "NOM001": "SRR341712",
        "NOM017": "SRR341720",
        "NOM027": "SRR341724",
        "NOM028": "SRR341725"}


    fastq_base, read_header, _ = fastaheader.split("_", 2)
    return fastq_basenames[fastq_base], read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_base+"_1.fastq", fastq_base+"_2.fastq"


