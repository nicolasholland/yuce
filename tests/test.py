import sys
from os.path import dirname
import unittest
import numpy as np

sys.path.append(dirname(dirname(__file__)))

import himawari
import gfs

class TestApp(unittest.TestCase):
    def test_himawari(self):
        img = himawari.getimage()
        self.assertTrue(isinstance(img, np.ndarray))

    def test_gfs(self):
        img = gfs.gfs()
        self.assertTrue(isinstance(img, np.ndarray))

if __name__ == '__main__':
    unittest.main()