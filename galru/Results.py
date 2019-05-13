import os
import csv


class Results:
    def __init__(self, mapping_output_file, metadata_file, extended_results):
        self.mapping_output_file = mapping_output_file
        self.metadata_file = metadata_file
        self.extended_results = extended_results

    def results(self, num_input_reads):
        if self.extended_results:
            return self.extended_results(num_input_reads)
        else:
            return self.summerised_results(num_input_reads)

    def summerised_results(self, num_input_reads):
        results = {}
        crispr_metadata = {}
        with open(self.metadata_file, newline="") as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter="\t")
            for row in metadata_reader:
                crispr_metadata[int(row[0])] = [row[1], row[2], row[3], row[4]]

        with open(self.mapping_output_file, newline="") as csvfile:
            mapping_reader = csv.reader(csvfile, delimiter="\t")
            for row in mapping_reader:
                st = crispr_metadata[int(row[2])][3]
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

    def extended_results(self):
        results = []
        crispr_metadata = {}
        with open(self.metadata_file, newline="") as csvfile:
            metadata_reader = csv.reader(csvfile, delimiter="\t")
            for row in metadata_reader:
                crispr_metadata[int(row[0])] = [row[1], row[2], row[3], row[4]]

        with open(self.mapping_output_file, newline="") as csvfile:
            mapping_reader = csv.reader(csvfile, delimiter="\t")
            for row in mapping_reader:
                result = "\t".join(
                    [
                        row[2],
                        row[4],
                        crispr_metadata[int(row[2])][0],
                        crispr_metadata[int(row[2])][2],
                        crispr_metadata[int(row[2])][3],
                    ]
                )
                results.append(result)
        return "\n".join(results)
