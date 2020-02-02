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

    def crispr_metadata_read(self):
        crispr_metadata = {}
        with open(self.metadata_file, newline="") as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter="\t")
            for row in metadata_reader:
                crispr_index = int(row[0])
                if crispr_index in crispr_metadata:
                    crispr_metadata[crispr_index].append([row[1], row[2], row[3], row[4]])
                else:
                    crispr_metadata[crispr_index] = [[row[1], row[2], row[3], row[4]]]
        return crispr_metadata
        

    def summerised_results(self, num_input_reads):
        results = {}
        crispr_metadata = self.crispr_metadata_read()

        for blast_result in self.blast_results:
            crispr_id = int(blast_result.query_name)
            sorted_sts = sorted(list(set([int(c[3]) for c in crispr_metadata[crispr_id] ])))
            st = ",".join([str(s) for s in sorted_sts])
            
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
        crispr_metadata = self.crispr_metadata_read()

        for blast_result in self.blast_results:
            crispr_id = int(blast_result.query_name)
            sorted_sts = sorted(list(set([int(c[3]) for c in crispr_metadata[crispr_id] ])))
            st = ",".join([str(s) for s in sorted_sts])
            
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
