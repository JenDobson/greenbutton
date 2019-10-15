import unittest
from unittest.mock import patch
import greenbutton.greenbutton as gb

import pandas as pd

class TestStringMethods(unittest.TestCase):
    
    def test_has_sample_data(self):
        self.assertTrue(isinstance(gb.SAMPLE_DATA,pd.DataFrame))
        
    def test_create_box_plot_of_use_by_hour(self):
        ax = gb.boxplot_use_by_hour(gb.SAMPLE_DATA)
        self.assertIsNotNone(ax)
        self.assertNotIn('Start Hour',gb.SAMPLE_DATA.columns)
        self.assertEqual(168,len(ax.lines))
            
    def test_bin_use_by_hour(self):
        pass
        
    
if __name__ == '__main__':
    unittest.main()
    