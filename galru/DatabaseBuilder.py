import os
import subprocess
import shutil
import re
import sys
from tempfile import mkstemp
from Bio import SeqIO
import hashlib

from galru.Mlst import Mlst


# Todo: merge crispr regions which are very close together and are probably the same feature.


class DatabaseBuilder:
    def __init__(
        self, input_files, output_directory, verbose, threads, allow_missing_st
    ):
        self.input_files = input_files
        self.output_directory = output_directory
        self.verbose = verbose
        self.threads = threads
        self.allow_missing_st = allow_missing_st
        self.files_to_cleanup = []

        self.combined_nucleotides = os.path.join(
            self.output_directory, "crispr_regions.fasta"
        )
        self.metadata_file = os.path.join(self.output_directory, "metadata.tsv")

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.minced_word_length = 9
        self.redirect_output = ""
        if self.verbose:
            self.redirect_output = ""
        else:
            self.redirect_output = " 2>&1"

        self.skipped_st = 0
        self.skipped_no_crispr = 0

    def find_crisprs_from_file(self, input_fasta):
        # uncompress file before passing to minced
        m = re.search(".gz$", input_fasta)
        if m:
            fd, input_fasta_uncompressed = mkstemp()
            cmd = " ".join(
                ["gunzip", "-c", input_fasta, ">" + input_fasta_uncompressed]
            )
            if self.verbose:
                print(cmd)
            subprocess.check_output(cmd, shell=True)
            self.files_to_cleanup.append(input_fasta_uncompressed)
            input_fasta = input_fasta_uncompressed

        fd, crispr_outputfile = mkstemp()
        crispr_gff_outputfile = crispr_outputfile + ".gff"
        self.files_to_cleanup.append(crispr_outputfile)
        self.files_to_cleanup.append(crispr_gff_outputfile)

        cmd = " ".join(
            [
                "minced",
                "-searchWL",
                str(self.minced_word_length),
                "-gff",
                input_fasta,
                crispr_gff_outputfile,
                self.redirect_output,
            ]
        )
        if self.verbose:
            print(cmd)

        subprocess.check_output(cmd, shell=True)
        return crispr_gff_outputfile

    def extract_nucleotides_from_gff(self, input_fasta, gff_file):
        m = re.search(".gz$", input_fasta)
        if m:
            fd, input_fasta_uncompressed = mkstemp()
            cmd = " ".join(
                ["gunzip", "-c", input_fasta, ">" + input_fasta_uncompressed]
            )
            if self.verbose:
                print(cmd)
            subprocess.check_output(cmd, shell=True)
            self.files_to_cleanup.append(input_fasta_uncompressed)
            input_fasta = input_fasta_uncompressed

        fd, outputfile = mkstemp()
        self.files_to_cleanup.append(outputfile)

        cmd = " ".join(
            [
                "bedtools",
                "getfasta",
                "-fo",
                outputfile,
                "-fi",
                input_fasta,
                "-bed",
                gff_file,
                self.redirect_output,
            ]
        )
        if self.verbose:
            print(cmd)

        subprocess.check_output(cmd, shell=True)
        return outputfile

    def next_sample_id(self, combined_nucleotides):
        if os.path.exists(combined_nucleotides):
            all_ids = []
            with open(combined_nucleotides, "r") as combined_nucleotides_fh:
                all_ids = [
                    int(record.id)
                    for record in SeqIO.parse(combined_nucleotides_fh, "fasta")
                ]
            return max(all_ids) + 1
        else:
            return 1

    def seq_to_names(self, combined_nucleotides):
        if os.path.exists(combined_nucleotides):
            all_ids = []
            with open(combined_nucleotides, "r") as combined_nucleotides_fh:
                all_seq = {
                    str(record.seq): int(record.id)
                    for record in SeqIO.parse(combined_nucleotides_fh, "fasta")
                }
            return all_seq
        else:
            return {}

    def append_crispr_file(
        self,
        crispr_nucleotides_file,
        input_fasta_file,
        combined_nucleotides,
        metadata_file,
        database,
        st,
    ):
        sequences_to_names = self.seq_to_names(combined_nucleotides)
        current_id = self.next_sample_id(combined_nucleotides)

        with open(combined_nucleotides, "a+") as combined_fh, open(
            metadata_file, "a+"
        ) as metadata_fh, open(crispr_nucleotides_file, "r") as crispr_nucleotides_fh:
            for record in SeqIO.parse(crispr_nucleotides_fh, "fasta"):
                if str(record.seq) in sequences_to_names:
                    record.id = str(sequences_to_names[record.seq])
                    metadata_fh.write(
                        "\t".join(
                            [
                                str(current_id),
                                os.path.basename(input_fasta_file),
                                record.description,
                                database,
                                st,
                            ]
                        )
                        + "\n"
                    )
                else:
                    record.id = str(current_id)
                    metadata_fh.write(
                        "\t".join(
                            [
                                str(current_id),
                                os.path.basename(input_fasta_file),
                                record.description,
                                database,
                                st,
                            ]
                        )
                        + "\n"
                    )
                    record.description = ""
                    SeqIO.write(record, combined_fh, "fasta")
                    sequences_to_names[str(record.seq)] = int(current_id)
                    current_id += 1

        return self

    def num_lines_in_file(self, filename):
        lines = 0
        with open(filename) as f:
            for l in f:
                lines += 1
        return lines

    def run(self):
        for f in self.input_files:
            mlst = Mlst(f, self.verbose, self.threads)
            if mlst.st == "-" and not self.allow_missing_st:
                self.skipped_st += 1
                if self.verbose:
                    print(str(f) + "\t" + "ST could not be determined, skipping")
                continue

            crispr_gff = self.find_crisprs_from_file(f)
            # GFF has a header
            if self.num_lines_in_file(crispr_gff) <= 1:
                self.skipped_no_crispr += 1
                if self.verbose:
                    print(str(f) + "\t" + "No CRISPRs found, skipping")
                continue

            crispr_nucleotides_file = self.extract_nucleotides_from_gff(f, crispr_gff)
            self.append_crispr_file(
                crispr_nucleotides_file,
                f,
                self.combined_nucleotides,
                self.metadata_file,
                mlst.database,
                mlst.st,
            )
            self.deleted_intermediate_files()

        return self

    def generate_stats(self):
        files_used = len(self.input_files) - self.skipped_st - self.skipped_no_crispr

        stats = [
            str(self.skipped_st),
            str(self.skipped_no_crispr),
            str(len(self.input_files)),
            str(files_used),
        ]
        return stats

    def deleted_intermediate_files(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
        self.files_to_cleanup = []

    def __del__(self):
        for f in self.files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
