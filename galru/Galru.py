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
        

    def run(self):
        num_reads, num_bases = self.count_reads_and_bases()
        cas_reads = self.reads_with_cas_genes()
        crispr_mapping = self.map_reads_to_crisprs(cas_reads)
        r = Results(crispr_mapping, self.metadata_file, True).summerised_results(num_reads)
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
            for record in SeqIO.parse(self.input_file, "fasta"):
                num_reads += 1 
                num_bases += len(record)
        return num_reads, num_bases
        

    def __del__(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
            
        