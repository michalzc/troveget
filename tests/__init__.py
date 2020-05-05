from unittest import TestCase
import os.path
import sys
import importlib.resources as pkg_resources
from . import testdata

import troveget

class TestTroveget(TestCase):


    def setUp(self):
        self.html_string = pkg_resources.read_text(testdata, 'index.html')
        

    def test_sth(self):
        self.assertEqual(1 + 2, 3)

    def test_parsing(self):

        self.assertTrue(self.html_string, "html should not be empty")
