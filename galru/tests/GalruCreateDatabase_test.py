import unittest
import os
import shutil
import filecmp
from galru.GalruCreateDatabase  import GalruCreateDatabase

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','galru_create_database')

class TestOptions:
    def __init__(self,input_files, output_directory, verbose):
        self.input_files = input_files
        self.output_directory = output_directory
        self.verbose = verbose
 
class TestGalruCreateDatabase(unittest.TestCase):
    def test_create_basic_database(self):
        
        if os.path.exists('output_db'):
            shutil.rmtree('output_db')
        g = GalruCreateDatabase(TestOptions([os.path.join(data_dir,'sample1.fa')], 'output_db', False))
        g.run()
        
        self.assertTrue(os.path.exists('output_db'))
        self.assertTrue(filecmp.cmp(os.path.join('output_db','crispr_regions.fasta'), os.path.join(data_dir,'expected_crispr_regions.fasta')))
        self.assertTrue(filecmp.cmp(os.path.join('output_db','metadata.tsv'), os.path.join(data_dir,'expected_metadata.tsv')))
        
        if os.path.exists('output_db'):
            shutil.rmtree('output_db')
        
        os.remove(os.path.join(data_dir,'sample1.fa') + '.fai')
        
        
    def test_create_basic_database_gzipped(self):
        
        if os.path.exists('output_db'):
            shutil.rmtree('output_db')
        g = GalruCreateDatabase(TestOptions([os.path.join(data_dir,'sample1.fa.gz')], 'output_db', False))
        g.run()
        
        self.assertTrue(os.path.exists('output_db'))
        self.assertTrue(filecmp.cmp(os.path.join('output_db','crispr_regions.fasta'), os.path.join(data_dir,'expected_crispr_regions.fasta')))
        self.assertTrue(filecmp.cmp(os.path.join('output_db','metadata.tsv'), os.path.join(data_dir,'expected_gz_metadata.tsv')))
        
        if os.path.exists('output_db'):
            shutil.rmtree('output_db')
