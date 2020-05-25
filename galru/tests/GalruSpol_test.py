import unittest
import os
import shutil
import filecmp
from galru.GalruSpol import GalruSpol

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, "data", "galru_spol")


class TestOptions:
    def __init__(
        self,
        species,
        input_file,
        db_dir,
        threads,
        technology,
        output_file,
        verbose,
        min_mapping_quality,
        debug, 
        gene_start_offset,
        extended_results
    ):
        self.species = species
        self.input_file = input_file
        self.db_dir = db_dir
        self.threads = threads
        self.technology = technology
        self.output_file = output_file
        self.verbose = verbose
        self.min_mapping_quality = min_mapping_quality
        self.debug = debug
        self.gene_start_offset = gene_start_offset
        self.extended_results = extended_results
        self.cas_fasta =  None
        self.qcov_margin = 100
        self.min_bitscore = 30
        self.min_identity = 95

class TestGalru(unittest.TestCase):
    def test_normal_analysis(self):
        g = GalruSpol(
            TestOptions(
                "Mycobacterium_tuberculosis",
                os.path.join(data_dir, "GCF_002886685.1_ASM288668v1.small"),
                None,
                1,
                "map-ont",
                "output_file",
                False,
                0,
                False,
                1000,
                False
            )
        )
        spoligotype = g.run()
        self.assertEqual(len(spoligotype), 43)
        self.assertEqual(spoligotype, '1111111101111111111000111111111100001111111')
        

        self.assertTrue(os.path.exists("output_file"))
        self.assertTrue(
            filecmp.cmp(os.path.join(data_dir, "expected_output_file"), "output_file")
        )
        os.remove("output_file")
