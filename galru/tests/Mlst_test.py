import unittest
import os
import shutil
import filecmp
from galru.Mlst import Mlst

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, "data", "mlst")


class TestMlst(unittest.TestCase):
    def test_mlst(self):
        m = Mlst(os.path.join(data_dir, "input.fa"), False, 1)
        self.assertEqual(m.database, "senterica")
        self.assertEqual(m.st, "3852")
