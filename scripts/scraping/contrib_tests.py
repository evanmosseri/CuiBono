import unittest
from contrib_data import *

class test_extract_name(unittest.TestCase):
    def test_texans_for(self):
        self.assertEqual(extract_filer_name("Texans for Rick Perry").strip(),"Rick Perry")