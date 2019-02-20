import os
import subprocess
import shutil
import re
from tempfile import mkstemp
from Bio import SeqIO

class GalruCreateDatabase:
    def __init__(self,options):
        self.input_files = options.input_files
        self.output_directory = options.output_directory
        self.verbose = options.verbose
        self.files_to_cleanup = []
        
        self.combined_nucleotides = os.path.join(self.output_directory, 'crispr_regions.fasta')
        self.metadata_file = os.path.join(self.output_directory, 'metadata.tsv')
        
        if os.path.exists(self.output_directory):
             print(
             "The output directory already exists, "
             "please choose another name: "
             + self.output_directory)
             sys.exit(1)
         
        else:
            os.makedirs(self.output_directory)
        
    def find_crisprs_from_file(self, input_fasta):    
        # uncompress file before passing to minced
        m = re.search(".gz$",input_fasta)
        if m:
            fd, input_fasta_uncompressed = mkstemp()
            cmd = " ".join(["gunzip", '-c'] + input_fasta + [ '>' + input_fasta_uncompressed])
            if self.verbose:
                print(cmd)
            subprocess.check_output( cmd, shell=True)
            self.files_to_cleanup.append(input_fasta_uncompressed)
            input_fasta = input_fasta_uncompressed

        fd, crispr_outputfile = mkstemp()
        crispr_gff_outputfile = crispr_outputfile + '.gff'
        self.files_to_cleanup.append(crispr_outputfile)
        self.files_to_cleanup.append(crispr_gff_outputfile)
        
        cmd = ' '.join(['minced', '-gff', input_fasta, crispr_gff_outputfile])
        if self.verbose:
            print(cmd)
        
        subprocess.check_output( cmd, shell=True)
        return crispr_gff_outputfile
        
    def extract_nucleotides_from_gff(self, input_fasta, gff_file):
        fd, outputfile = mkstemp()
        self.files_to_cleanup.append(outputfile)
        
        cmd = ' '.join(['bedtools', 'getfasta', '-fo', outputfile, '-fi', input_fasta, '-bed', gff_file])
        if self.verbose:
            print(cmd)
        
        subprocess.check_output( cmd, shell=True)
        return outputfile
        
    def next_sample_id(self, combined_nucleotides):
        if os.path.exists(combined_nucleotides):
            all_ids = [int(record.id) for record in SeqIO.parse(combined_nucleotides, "fasta")]
            return max(all_ids) + 1
        else:
            return 1
        
    def append_crispr_file(self, crispr_nucleotides_file, input_fasta_file, combined_nucleotides, metadata_file):
        current_id = self.next_sample_id(combined_nucleotides)
            
        with open(combined_nucleotides, "a+") as combined_fh, open(metadata_file, "a+") as metadata_fh:
            for record in SeqIO.parse(crispr_nucleotides_file, "fasta"):
                record.id = str(current_id)
                metadata_fh.write("\t".join([str(current_id), os.path.basename(input_fasta_file), record.description]) + "\n")
                record.description = ''
                SeqIO.write(record, combined_fh, "fasta")
                current_id += 1
                
        return self              
        
    def run(self):
        for f in self.input_files:
            crispr_gff = self.find_crisprs_from_file(f)
            crispr_nucleotides_file = self.extract_nucleotides_from_gff(f, crispr_gff)
            self.append_crispr_file( crispr_nucleotides_file, f, self.combined_nucleotides, self.metadata_file)
        
        return self

    def __del__(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
            
        