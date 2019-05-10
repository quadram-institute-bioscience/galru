import os
import subprocess
import shutil
from tempfile import mkstemp


class GalruCreateCas:
    def __init__(self, options):
        self.input_files = options.input_files
        self.output_filename = options.output_filename
        self.verbose = options.verbose
        self.threads = options.threads
        self.cdhit_seq_identity = options.cdhit_seq_identity
        self.debug = options.debug
        self.files_to_cleanup = []

    # ToDo: Find Cas genes in a more intelligent way
    def filter_single_file(self, filename):
        fd, single_filtered_outputfile = mkstemp()
        self.files_to_cleanup.append(single_filtered_outputfile)

        cmd = " ".join(
            [
                "fastaq",
                "get_ids",
                filename,
                "-",
                "|",
                "grep",
                "Cas",
                "|",
                "awk",
                "'{print $1}'",
                "|",
                "fastaq",
                "filter",
                "--ids_file",
                "-",
                filename,
                single_filtered_outputfile,
            ]
        )
        if self.verbose:
            print("Extract CAS genes:\t" + cmd)

        subprocess.check_output(cmd, shell=True)
        os.close(fd)
        return single_filtered_outputfile

    # do it one file at a time so that you dont hit the limit on filenames passed on command line. Its a minor inefficiency.
    def concat_files(self, filenames):
        fd, concat_outputfile = mkstemp()
        self.files_to_cleanup.append(concat_outputfile)

        for f in filenames:
            cmd = " ".join(["cat", f, ">>", concat_outputfile])
            if self.verbose:
                print(cmd)
            subprocess.check_output(cmd, shell=True)
        os.close(fd)
        return concat_outputfile

    def cluster_genes(self, input_fasta):
        fd, compress_outputfile = mkstemp()
        # The temp fasta file gets moved so no need to clean it up
        self.files_to_cleanup.append(compress_outputfile + ".clstr")

        cmd = " ".join(["cd-hit-est", "-T",str(self.threads), "-c", str(self.cdhit_seq_identity), "-i", input_fasta, "-o", compress_outputfile])
        if self.verbose:
            print("Clustering the CAS genes:\t" + cmd)

        subprocess.check_output(cmd, shell=True)
        os.close(fd)
        return compress_outputfile

    def run(self):
        # filter out just the 'Cas' gene sequences
        # This step could be run in parallel
        cas_fastas = []
        for f in self.input_files:
            cas_fastas.append(self.filter_single_file(f))

        merged_cas_fasta = self.concat_files(cas_fastas)
        clustered_fasta = self.cluster_genes(merged_cas_fasta)
        if os.path.exists(clustered_fasta):
            shutil.move(clustered_fasta, self.output_filename)
            
            cmd = " ".join(["gzip", self.output_filename])
            if self.verbose:
                print("Compressing CAS gene FASTA file:\t" + cmd)
            subprocess.check_output(cmd, shell=True)
            
        else:
            print("Failed to create file")
        return self

    def __del__(self):
        if not self.debug:
            for f in self.files_to_cleanup:
                if os.path.exists(f):
                    os.remove(f)
