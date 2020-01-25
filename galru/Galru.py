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

# map all the reads to the Cas genes. Any reads that map are them mapped against the CRISPRs

class Galru:
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
            self.database_directory, "cas.fa.gz"
        )

        self.files_to_cleanup = []

        self.crisprs_file = os.path.join(
            self.database_directory, "crispr_regions.fasta"
        )
        self.metadata_file = os.path.join(self.database_directory, "metadata.tsv")

        self.redirect_output = ""
        if self.verbose:
            self.redirect_output = ""
        else:
            self.redirect_output = " 2>&1"

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
                "-a",
                self.cas_fasta,
                self.input_file,
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

    # blast the crisprs against the reads
    def map_reads_to_crisprs(self, cas_reads):
        # Create a blast database out of the reads
        blastdatabase = BlastDatabase(cas_reads, self.verbose)
        blast = Blast(blastdatabase.db_prefix, self.threads, 100 - self.qcov_margin,  self.min_identity, self.verbose)
        blast_results = blast.run_blast(self.crisprs_file)
        best_hits = BlastFilter(blast_results, self.qcov_margin, self.min_bitscore).best_hit_for_each_read()
        
        return best_hits

    def run(self):
        num_reads, num_bases = self.count_reads_and_bases()
        cas_reads = self.reads_with_cas_genes()
        crispr_blast = self.map_reads_to_crisprs(cas_reads)
        r = Results(crispr_blast, self.metadata_file, self.extended_results).results(
            num_reads
        )
        print(r)

        if self.output_file is not None:
            with open(self.output_file, "w") as out_fh:
                out_fh.write(r)

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
