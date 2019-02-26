import os
import subprocess
import shutil
import sys
import csv
from tempfile import mkstemp
from Bio import SeqIO

from galru.Schemas import Schemas

# map all the reads to the Cas genes. Any reads that map are them mapped against the CRISPRs

class Galru:
    def __init__(self,options):
        self.input_file = options.input_file
        self.cas_fasta = options.cas_fasta
        self.verbose = options.verbose
        self.output_file = options.output_file
        self.technology = options.technology
        
        self.database_directory =  Schemas().database_directory(options.db_dir, options.species)
        
        if self.cas_fasta is None:
            self.cas_fasta = str(pkg_resources.resource_filename( __name__, 'data/cas.fa.gz'))
        
        self.files_to_cleanup = []
        
        self.crisprs_file = os.path.join(self.database_directory, 'crispr_regions.fasta')
        self.metadata_file = os.path.join(self.database_directory, 'metadata.tsv')
        
        self.redirect_output = ''
        if self.verbose:
            self.redirect_output = ''
        else:
            self.redirect_output = ' 2>&1'
        
    # map the raw reads to the clustered cas genes = gives reads containing cas genes
    def reads_with_cas_genes(self):
        fd, reads_outputfile = mkstemp()
        self.files_to_cleanup.append(reads_outputfile)
        
        cmd = ' '.join(['minimap2', '-x', self.technology, '-a',  self.cas_fasta, self.input_file, '|', 'samtools', 'fasta', '-F', '4', '-', '>', reads_outputfile, self.redirect_output])
        if self.verbose:
            print(cmd)
        
        subprocess.check_output( cmd, shell=True)
        return reads_outputfile

    # map the cas gene reads to the reference database of crisprs
    def map_reads_to_crisprs(self, cas_reads):
        fd, reads_outputfile = mkstemp()
        self.files_to_cleanup.append(reads_outputfile)

        cmd = ' '.join(['minimap2', '-x', self.technology, '-a',  self.crisprs_file, cas_reads, '|', 'samtools', 'view', '-F', '4', '-', '>', reads_outputfile, self.redirect_output])
        if self.verbose:
            print(cmd)
        
        subprocess.check_output( cmd, shell=True)
        return reads_outputfile
        
    def print_results(self, mapping_output_file):
        results = []
        crispr_metadata = {}
        with open(self.metadata_file, newline='') as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter='\t')
            for row in metadata_reader:
                crispr_metadata[int(row[0])] = [row[1], row[2], row[3], row[4]]
                
        with open(mapping_output_file, newline='') as csvfile:
            mapping_reader = csv.reader(csvfile, delimiter='\t')
            for row in mapping_reader:
                result = "\t".join([row[2],row[4],crispr_metadata[int(row[2])][0], crispr_metadata[int(row[2])][2],crispr_metadata[int(row[2])][3]  ])
                results.append(result)
        print("\n".join(results))
        

    def run(self):
        cas_reads = self.reads_with_cas_genes()
        crispr_mapping = self.map_reads_to_crisprs(cas_reads)
        self.print_results(crispr_mapping)
        
        return self

    def __del__(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
            
        