import re
import os
import subprocess
import shutil
from tempfile import mkdtemp
from galru.DatabaseBuilder import DatabaseBuilder
from galru.GalruCreateCas import GalruCreateCas


class CasOptions:
    def __init__(self, input_files, output_filename, verbose, cdhit_seq_identity, debug, threads ):
        self.input_files = input_files
        self.output_filename = output_filename
        self.verbose = verbose
        self.cdhit_seq_identity = cdhit_seq_identity
        self.debug = debug
        self.threads = threads

class GalruCreateSpecies:
    def __init__(self, options):
        self.species = options.species
        self.output_directory = options.output_directory
        self.verbose = options.verbose
        self.threads = options.threads
        self.allow_missing_st = options.allow_missing_st
        self.cdhit_seq_identity = options.cdhit_seq_identity
        self.assembly_level = options.assembly_level
        self.debug = options.debug
        self.refseq_category = options.refseq_category

        if self.output_directory is None:
            self.output_directory = re.sub("[^a-zA-Z0-9]+", "_", self.species)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.directories_to_cleanup = []

    def download_species(self):
        download_directory = str(mkdtemp(dir=self.output_directory))
        self.directories_to_cleanup.append(download_directory)

        cmd = " ".join(
            [
                "ncbi-genome-download",
                "-o",
                download_directory,
                "--genus",
                '"' + self.species + '"',
                "--parallel",
                str(self.threads),
                "--assembly-level",
                self.assembly_level,
                "-R",
                self.refseq_category,
                "-F",
                "fasta,cds-fasta",
                "bacteria",
            ]
        )
        if self.verbose:
            print("Download genomes from NCBI:\t"+ cmd)
        subprocess.check_output(cmd, shell=True)
        return download_directory

    def find_input_files(self, download_directory):
        input_files = []
        for root, dirs, files in os.walk(download_directory):
            for file in files:
                if file.endswith("genomic.fna.gz"):
                    input_files.append(os.path.join(root, file))
        return input_files
        
    def find_cds_fasta_files(self, download_directory):
        input_files = []
        for root, dirs, files in os.walk(download_directory):
            for file in files:
                if file.endswith("cds_from_genomic.fna.gz"):
                    input_files.append(os.path.join(root, file))
        return input_files

    def run(self):
        download_directory = self.download_species()
        input_files = self.find_input_files(download_directory)

        database_builder = DatabaseBuilder(
            input_files,
            self.output_directory,
            self.verbose,
            self.threads,
            self.allow_missing_st,
            self.debug
        )
        database_builder.run()
        print(self.species + "\t" + "\t".join(database_builder.generate_stats()))
        
        # build CAS database for species
        cas_input_files = self.find_cds_fasta_files(download_directory)
        
        g = GalruCreateCas(
            CasOptions(
                input_files,
                os.path.join(self.output_directory, "cas.fa"),
                self.verbose,
                self.cdhit_seq_identity,
                self.debug,
                self.threads
            )
        )
        g.run()

    def __del__(self):
        if not self.debug:
            for d in self.directories_to_cleanup:
                if os.path.exists(d):
                    shutil.rmtree(d)
