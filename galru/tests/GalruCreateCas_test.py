import unittest
import os
import shutil
import filecmp
from galru.GalruCreateCas import GalruCreateCas

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, "data", "galru_create_cas")


class TestOptions:
    def __init__(self, input_files, output_filename, verbose, cdhit_seq_identity,debug, threads):
        self.input_files = input_files
        self.output_filename = output_filename
        self.verbose = verbose
        self.cdhit_seq_identity = cdhit_seq_identity
        self.debug = debug
        self.threads = threads


class TestGalruCreateCas(unittest.TestCase):
    def test_create_basic_database(self):
        g = GalruCreateCas(
            TestOptions(
                [
                    os.path.join(data_dir, "file1.fa"),
                    os.path.join(data_dir, "file2.fa"),
                ],
                "output_filename",
                False,
                0.9,
                False,
                1
            )
        )
        g.run()
        self.assertTrue(os.path.exists("output_filename"))
        self.assertTrue(
            filecmp.cmp(
                "output_filename", os.path.join(data_dir, "expected_output_filename")
            )
        )

        if os.path.exists("output_filename"):
            os.remove("output_filename")
