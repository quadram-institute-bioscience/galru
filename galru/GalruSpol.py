import os
import subprocess
import shutil
import sys
import re
import gzip
import pkg_resources
from tempfile import mkstemp
from Bio import SeqIO
from galru.Results import Results
from galru.Schemas import Schemas
from galru.Blast import Blast
from galru.BlastDatabase import BlastDatabase
from galru.BlastResult import BlastResult
from galru.BlastFilter import BlastFilter

class GalruSpol:
    def __init__(self, options):
        self.input_file = options.input_file
        self.cas_fasta = options.cas_fasta
        self.verbose = options.verbose
        self.output_file = options.output_file
        self.technology = options.technology
        self.threads = options.threads
        self.min_mapping_quality = options.min_mapping_quality
        self.debug = options.debug
        self.gene_start_offset = options.gene_start_offset
        self.extended_results = options.extended_results
        self.qcov_margin = options.qcov_margin
        self.min_bitscore = options.min_bitscore
        self.min_identity = options.min_identity

        self.database_directory = Schemas().database_directory(
            options.db_dir, options.species
        )

        if self.cas_fasta is None:
            self.cas_fasta = os.path.join(
            self.database_directory, "crispr_regions.fasta"
        )

        self.files_to_cleanup = []

        self.crisprs_file = os.path.join(
            self.database_directory, "spacers.fasta"
        )
        self.metadata_file = os.path.join(self.database_directory, "metadata.tsv")

        self.redirect_output = ""
        if self.verbose:
            self.redirect_output = ""
        else:
            self.redirect_output = " 2>/dev/null "

    # map the raw reads to the clustered cas genes = gives reads containing cas genes
    def reads_with_cas_genes(self):
        fd, reads_outputfile = mkstemp()
        self.files_to_cleanup.append(reads_outputfile)

        cmd = " ".join(
            [
                "minimap2",
                "-x",
                self.technology,
				"-t",
				str(self.threads),
                "--secondary=no",
                "-a",
                self.cas_fasta,
                self.input_file,
                self.redirect_output,
                "|",
                "samtools",
                "fasta",
				"--threads",
				str(self.threads),
                "-F",
                "4",
                "-",
                ">",
                reads_outputfile,
                self.redirect_output,
            ]
        )
        if self.verbose:
            print("Identify reads containing CAS genes:\t" + cmd)

        subprocess.check_output(cmd, shell=True)
        os.close(fd)
        return reads_outputfile
        
    def map_crisprs_to_reads(self, cas_reads):
        blastdatabase = BlastDatabase(self.crisprs_file, self.verbose)
        blast = Blast(blastdatabase.db_prefix, self.threads, 0,  self.min_identity, self.verbose, word_size = 9, exec = 'blastn', evalue = 0.000001,  task = 'blastn-short')
        blast_results = blast.run_blast(cas_reads)
        crispr_ids = BlastFilter(blast_results, 100, self.min_bitscore).crispr_ids()
        
        fdcff, crisprs_filtered_file = mkstemp()
        self.files_to_cleanup.append(crisprs_filtered_file)
        
        with open(self.crisprs_file, "r") as in_handle, open(crisprs_filtered_file, "a+") as out_fh:
            for record in SeqIO.parse(in_handle, "fasta"):
                if record.id in crispr_ids:
                    SeqIO.write(record, out_fh, "fasta")
        
        fd, crisprs_outputfile = mkstemp()
        self.files_to_cleanup.append(crisprs_outputfile)

        os.close(fd)
        os.close(fdcff)
        return crisprs_filtered_file

    # blast the crisprs against the reads
    def blast_crisprs_to_reads(self, cas_reads, filtered_crisprs):
        # Create a blast database out of the reads
        blastdatabase = BlastDatabase(cas_reads, self.verbose)
        blast = Blast(blastdatabase.db_prefix, self.threads, 100 - self.qcov_margin,  self.min_identity, self.verbose,  word_size = 9, exec = 'blastn', evalue = 0.000001,  task = 'blastn-short')
        blast_results = blast.run_blast(filtered_crisprs)
        
        bf = BlastFilter(blast_results, self.qcov_margin, self.min_bitscore)
        spoligotype = bf.spoligotype()
        
        return "".join([str(s) for s in spoligotype])

    def run(self):
        num_reads, num_bases = self.count_reads_and_bases()
        cas_reads = self.reads_with_cas_genes()
        filtered_crisprs = self.map_crisprs_to_reads(cas_reads)
        spoligotype = self.blast_crisprs_to_reads(cas_reads, filtered_crisprs)
        print(spoligotype)
        
        if self.output_file is not None:
            with open(self.output_file, "w") as out_fh:
                out_fh.write(spoligotype)

        return self

    def count_reads_and_bases(self):
        num_reads = 0
        num_bases = 0

        m = re.search(r".gz$", self.input_file)
        if m:
            with gzip.open(self.input_file, "rt") as handle:
                for record in SeqIO.parse(handle, "fasta"):
                    num_reads += 1
                    num_bases += len(record)
        else:
            with open(self.input_file, "r") as handle:
                for record in SeqIO.parse(handle, "fasta"):
                    num_reads += 1
                    num_bases += len(record)
        return num_reads, num_bases

    def __del__(self):
        if not self.debug:
            for f in self.files_to_cleanup:
                if os.path.exists(f):
                    os.remove(f)
