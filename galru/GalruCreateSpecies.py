import re
import os
import subprocess
import shutil
from tempfile import mkdtemp
from galru.DatabaseBuilder import DatabaseBuilder

class GalruCreateSpecies:
    def __init__(self,options):
        self.species = options.species
        self.output_directory = options.output_directory
        self.verbose = options.verbose  
        self.threads = options.threads  
        self.allow_missing_st = options.allow_missing_st
        
        if self.output_directory is None:
            self.output_directory = re.sub("[^a-zA-Z0-9]+", "_", self.species)
            
        self.directories_to_cleanup = []
        
    def download_species(self):
        download_directory = mkdtemp(dir=self.output_directory)
        
        cmd = " ".join(['ncbi-genome-download', '-o', download_directory, '--genus', '"'+ self.species +'"', '--parallel', self.threads, '-F', 'fasta', 'bacteria'])
        if self.verbose:
            print(cmd)
        subprocess.check_output( cmd, shell=True)
        return download_directory
        
    def find_input_files(self,download_directory):
        input_files = []
        for root, dirs, files in os.walk(download_directory):
            for file in files:
                if file.endswith("genomic.fna.gz"):
                     input_files.append(os.path.join(root, file))
        return input_files

    def run(self):
        download_directory = self.download_species()
        input_files = self.find_input_files(download_directory)
        
        database_builder = DatabaseBuilder(input_files,  self.output_directory,  self.verbose,  self.threads,  self.allow_missing_st)
        database_builder.run()
        database_builder.print_stats()
        
    def __del__(self):
        for d in self.directories_to_cleanup:
            if os.path.exists(d):
                shutil.rmtree(d)
                