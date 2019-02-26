import subprocess
import csv

class Mlst:
    
    def __init__(self, filename, verbose, threads):
        self.filename = filename
        self.verbose = verbose
        self.threads = threads
        self.script_output = self.mlst_output()
        self.database, self.st = self.parse_output(self.script_output)
    	
    def mlst_output(self):
        cmd = " ".join(["mlst", '--nopath','--quiet', self.filename])
        if self.verbose:
            print(cmd)
        output = subprocess.check_output( cmd, shell=True)
        return output.decode("utf-8") 
        
    def parse_output(self, mlst_text):
        if mlst_text is not '' and mlst_text is not None:
            for row in csv.reader([mlst_text], delimiter='\t'):
                return row[1], row[2]
        return '-','-'
        