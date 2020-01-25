import os
from os import listdir
from os.path import isfile, join
import re
from tempfile import mkstemp
from tempfile import mkdtemp
import subprocess
import shutil

class BlastDatabase:
    def __init__(self, input_file, verbose):
        self.input_file = input_file
        self.verbose = verbose
        self.db_prefix = self.make_blastdb(self.input_file)
        
     # make a blast database
    def make_blastdb(self, input_file):
        tmpdir = mkdtemp()
        output_prefix = os.path.join(tmpdir, 'all')
        cmd = " ".join(['makeblastdb', '-in', input_file, '-dbtype', 'nucl',  '-out', output_prefix])
        if self.verbose:
            print("Creating blast database:\t" + cmd)
        subprocess.check_output(cmd, shell=True)
        return output_prefix
    
    def __del__(self):
        if os.path.exists(self.db_prefix):
            shutil.rmtree(self.db_prefix)
            