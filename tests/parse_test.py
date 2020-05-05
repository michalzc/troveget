import importlib.resources as pkg_resources
import os.path
import sys
from unittest import TestCase

from troveget.troveparse import find_links
from tests import testdata


class TestParseTroveget(TestCase):

    def setUp(self):
        self.html_string = pkg_resources.read_text(testdata, 'index.html')
        

    def test_find_links(self):
        (dir_links, file_links) = find_links(self.html_string)
        self.assertTrue(dir_links, "dir links shoould not be empty")
        self.assertTrue(file_links, "file links should not be empty")