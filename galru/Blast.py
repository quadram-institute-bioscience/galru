from tempfile import mkstemp
import subprocess
import os
import re

class Blast:
    def __init__(self, blast_db, threads, qcov_hsp_perc, min_identity, verbose, word_size = 28, exec = 'blastn', evalue = 0.0000000001,  task = 'megablast'):
        self.blast_db = blast_db
        self.evalue = evalue
        self.threads = threads
        self.word_size = word_size
        self.min_identity = min_identity
        self.qcov_hsp_perc = qcov_hsp_perc
        self.exec = exec
        self.task = task
        self.verbose = verbose
        self.files_to_cleanup = []

    def decompress_file_to_tmp(self, input_file):
        m = re.search(r".gz$", input_file)
        if m:
            fd, decompressed_input_file = mkstemp()
            self.files_to_cleanup.append(decompressed_input_file)
            cmd = " ".join(['gunzip', '-c', input_file, '>', decompressed_input_file])
            if self.verbose:
                print("Decompress file before blasting:\t" + cmd)
            subprocess.check_output( cmd,  shell=True)
            
            return decompressed_input_file
        else:
            return input_file

    def blast_command(self, query, blast_results):   
        return " ".join([self.exec, '-outfmt', '"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs qcovhsp"', 
        '-evalue', str(self.evalue), 
        '-db', self.blast_db, '-word_size', str(self.word_size), 
        '-num_threads', str(self.threads), '-task', self.task, 
        '-perc_identity', str(self.min_identity),
        '-query', self.decompress_file_to_tmp(query), '-out', blast_results])
        
    def run_blast(self, query):
        fd, blast_results = mkstemp()
        cmd = self.blast_command(query, blast_results)
        if self.verbose:
            print("Run blastn:\t" + cmd )
        subprocess.check_output( cmd,  shell=True)
        os.close(fd)
        return blast_results

    def __del__(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)    
                