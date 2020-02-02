import re
import os
import subprocess
import shutil
import csv
from tempfile import mkstemp
from galru.DatabaseBuilder import DatabaseBuilder
from galru.GalruCreateCas import GalruCreateCas
from galru.Schemas import Schemas

class Cluster:
    def __init__(self):
        self.centroid = None
        self.other_ids = []

class GalruShrinkDatabase:
    def __init__(self, options):
        self.percentage_similarity = options.percentage_similarity
        self.output_filename = options.output_filename
        self.debug = options.debug
        self.verbose = options.verbose
        self.files_to_cleanup = []

        self.database_directory = Schemas().database_directory(
            options.db_dir, options.species
        )

        self.crisprs_file = os.path.join(
            self.database_directory, "crispr_regions.fasta"
        )
        self.metadata_file = os.path.join(self.database_directory, "metadata.tsv")


    def run(self):
        crispr_clusters_fasta_file = self.cluster_crisprs()
        all_clusters = self.read_cdhit_clusters(crispr_clusters_fasta_file+'.clstr')
        self.update_metadata_file( self.metadata_file, self.output_filename, all_clusters)

    def cluster_crisprs(self):
        fd, crispr_output = mkstemp()
        self.files_to_cleanup.append(crispr_output)
        self.files_to_cleanup.append(crispr_output + '.clstr')
        
        # cd-hit-est
        cmd = "cd-hit-est -g 1 -s " + str(self.percentage_similarity) +  " -c " + str(self.percentage_similarity) +  " -i " + str(self.crisprs_file) + " -o " + crispr_output
        subprocess.check_output(cmd, shell=True)
        os.close(fd)
        
        return crispr_output
    
    #>Cluster 1220
    #0       823nt, >221... at +/95.02%
    #1       822nt, >222... at +/95.13%
    #2       883nt, >260... *
    #3       822nt, >328... at -/95.13%
    #4       883nt, >387... at +/90.94%
    #5       883nt, >388... at +/93.20%
    #6       822nt, >1270... at +/95.26%
    #7       822nt, >7019... at -/94.65%
    def read_cdhit_clusters(self, filename):
        all_clusters = []
        with open(filename, "r") as clusters_fh:
            lines = clusters_fh.readlines()
            
            current_cluster = Cluster()
            for line in lines:
                m = re.match(r">Cluster", line)
                
                # start of new cluster
                if m:
                    # save old cluster
                    all_clusters.append(current_cluster)
                    
                    # create new cluster 
                    current_cluster = Cluster()
                    
                else:
                    # within a cluster
                    m = re.search(r", >([\d]+)... (.)", line)
                    if m:
                        if m.group(2) == 'a':
                            current_cluster.other_ids.append(int(m.group(1)))
                        else:
                            current_cluster.centroid = int(m.group(1))
                
            all_clusters.append(current_cluster)
        return all_clusters
        
        
    def update_metadata_file(self, input_filename, output_filename, clusters):
        cluster_ids_to_representative = {}
        for cluster in clusters:
            for c in cluster.other_ids:
                cluster_ids_to_representative[c] = cluster.centroid
        
        lines = None
        output_lines = []
        with open( input_filename, "r") as md_read_fh, open( output_filename, "w+") as md_write_fh:
            metadata_reader = csv.reader(md_read_fh, delimiter="\t")
            for row in metadata_reader:
                crispr_id = int(row[0])
                if crispr_id in cluster_ids_to_representative:
                    output_lines.append(
                        "\t".join(
                            [
                                str(cluster_ids_to_representative[crispr_id]),
                                row[1],
                                row[2],
                                row[3],
                                row[4]
                            ]
                        ))
                else:
                    output_lines.append( "\t".join(row) )
            
            md_write_fh.write("\n".join(sorted(output_lines)))

    def __del__(self):
        if not self.debug:
            for f in self.files_to_cleanup:
                if os.path.exists(f):
                    os.remove(f)
        
        