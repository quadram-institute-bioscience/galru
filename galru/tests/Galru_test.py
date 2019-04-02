import unittest
import os
import shutil
import filecmp
from galru.Galru import Galru

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, "data", "galru")


class TestOptions:
    def __init__(
        self,
        species,
        input_file,
        db_dir,
        cas_fasta,
        threads,
        technology,
        output_file,
        verbose,
    ):
        self.species = species
        self.input_file = input_file
        self.db_dir = db_dir
        self.cas_fasta = cas_fasta
        self.threads = threads
        self.technology = technology
        self.output_file = output_file
        self.verbose = verbose


class TestGalru(unittest.TestCase):
    def test_normal_analysis(self):
        g = Galru(
            TestOptions(
                "Salmonella",
                os.path.join(data_dir, "uncorrected_reads.fasta.gz"),
                data_dir,
                os.path.join(data_dir, "cas.fa.gz"),
                1,
                "map-ont",
                "output_file",
                False,
            )
        )
        g.run()

        self.assertTrue(os.path.exists("output_file"))
        self.assertTrue(
            filecmp.cmp(os.path.join(data_dir, "expected_output_file"), "output_file")
        )
        os.remove("output_file")
