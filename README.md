# Assembling qnr
This README explains the basic steps in re-assembling contiguous qnr sequences from identified metagenomic reads.

The process consists of several steps:

## 1. Extract sequences from FASTQ
Go back to the complete original raw reads in the FASTQ data.  First, write a
*transformer* that understands how to parse the FASTA headers into FASTQ
filenames and FASTQ headers. Then do something like this:

    :::bash
	extract_sequences_from_fastq.py \
	   --fasta /path/to/fasta/files*.fasta \
	   --fastq-dir /path/to/raw/fastq_dir/ \
	   --transformer <name_of_transformer> \
	   --left <output_left.fastq> \
	   --right <output_right.fastq>

You can expect this to take a while, depending on the size of all the FASTQ
files. 
	
## 2. Run the Snakemake workflow
In the folder where you put `<output_left.fastq>` and `<output_right.fastq>`,
create the following folder and put the files like this:

    ./
	./pmqr.hmm     <-- HMMER hidden Markov model for qnr
	./pmqr.pfa     <-- Protein sequences of all known plasmid mediated qnr
	./selected_reads/left.fastq    <-\
	./selected_reads/right.fastq   <--The two files you just created

Running snakemake to perform the assembly and first step validation is now as
easy as running this command in the folder:

	snakemake -s /path/to/extract_best_domains.snakemake

The snakefile requires that the following programs (and commands) are available on PATH:

   - trim_galore (`trim_galore`)
   - SPAdes (`spades.py`)
   - HMMer (`hmmsearch`)
   - Easel (`esl-sfetch`)
   - Clustal Omega (`clustalo`)
   - `extract_from_fasta.py`
   - `get_most_similar_pmqr.py`


## 3. Analyze output
The first thing to look at is the file `results/most_similar_qnr.txt` that shows if any
of the contigs (longer than 200 aa) are identical to any know plasmid mediated qnr.

The second thing to look at is the file `results/four_most_similar_qnr.txt` that shows
the level of similarity with known plasmid mediated qnr. 

The third thing to do is to run the interesting contig domains against e.g. GenBank via
BLASTP to see if there are any identical hits in GenBank. If there isn't, there is a big
chance that the identified contig domain is a putative qnr.
