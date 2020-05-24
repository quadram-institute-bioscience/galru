from galru.BlastResult import BlastResult
import csv 

class BlastFilter:
    def __init__(self, blast_results_file, qcov_margin, min_bitscore):
        self.blast_results_file = blast_results_file
        self.qcov_margin = qcov_margin
        self.min_bitscore = min_bitscore
        self.unfiltered_results = self.readin_results()
        
    def readin_results(self):
        results = []
        with open(self.blast_results_file , newline='') as blastfile:
            blastreader = csv.reader(blastfile, delimiter='\t')
            for row in blastreader:
                results.append(BlastResult(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
        return results
        
    def filter_results(self):
        filtered = []
        qcov_min = 100 - self.qcov_margin
        qcov_max = 100 + self.qcov_margin
        for result in self.unfiltered_results:
            if result.qcov >=  qcov_min and result.qcov <= qcov_max and result.bit_score >= self.min_bitscore:
                filtered.append(result)
        return filtered
    
    def crispr_ids(self):
        crispr_freq = {}
        for result in self.filter_results():
            if result.subject in crispr_freq:
                crispr_freq[result.subject] += 1
            else:
                crispr_freq[result.subject] = 1 
        return crispr_freq.keys()
        
    def spoligotype(self):     
        typing = []           
        found_spacers = {int(result.query_name):1 for result in self.filter_results()}
            
        for i in range(1,43):
            if i in found_spacers:
                typing.append(1)
                
            else:
                typing.append(0)
            
        return typing 
    
   
    def best_hit_for_each_read(self):
        read_best_hit = {}
        
        for result in self.filter_results():
            if result.subject in read_best_hit:
                if result.bit_score > read_best_hit[result.subject].bit_score:
                    read_best_hit[result.subject] = result
            else:
                read_best_hit[result.subject] = result
                
        return read_best_hit.values()
 