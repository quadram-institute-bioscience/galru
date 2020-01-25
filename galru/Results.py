import os
import csv
import sys


class Results:
    def __init__(self, blast_results, metadata_file, extended_results):
        self.blast_results = blast_results
        self.metadata_file = metadata_file
        self.extended_results = extended_results

    def results(self, num_input_reads):
        if self.extended_results:
            return self.full_extended_results(num_input_reads)
        else:
            return self.summerised_results(num_input_reads)

    def summerised_results(self, num_input_reads):
        results = {}
        crispr_metadata = {}
        with open(self.metadata_file, newline="") as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter="\t")
            for row in metadata_reader:
                crispr_metadata[int(row[0])] = [row[1], row[2], row[3], row[4]]

        for blast_result in self.blast_results:
            st = crispr_metadata[int(blast_result.query_name)][3]
            if st in results:
                results[st] += 1
            else:
                results[st] = 1
            
        sorted_results = ["ST\tNo. Reads\tInput Reads"]
        sorted_sts = sorted(results.items(), reverse=True, key=lambda x: x[1])
        for (st, st_freq) in sorted_sts:
            sorted_results.append(
                str(st) + "\t" + str(st_freq) + "\t" + str(num_input_reads)
            )

        return "\n".join(sorted_results)

    def full_extended_results(self, num_input_reads):
        results = []
        crispr_metadata = {}
        with open(self.metadata_file, newline="") as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter="\t")
            for row in metadata_reader:
                crispr_metadata[int(row[0])] = [row[1], row[2], row[3], row[4]]

        for blast_result in self.blast_results:
            crispr_id = int(blast_result.query_name)
            st = crispr_metadata[int(blast_result.query_name)][3]
            
            result = "\t".join(
                [
                    str(st),
                    str(blast_result.subject),
                    str(blast_result.bit_score),
                    str(blast_result.identity),
                    str(blast_result.qcov),
                    str(blast_result.qcovhsp),
                    str(crispr_metadata[crispr_id][0]),
                    str(crispr_metadata[crispr_id][2]),
                    str(crispr_metadata[crispr_id][3]),
                ]
            )
            results.append(result)
        return "\n".join(results)
