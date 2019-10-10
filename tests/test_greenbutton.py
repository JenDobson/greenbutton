import unittest
import greenbutton.greenbutton as gb

import pandas as pd

class TestStringMethods(unittest.TestCase):
    
    def test_has_sample_data(self):
        self.assertTrue(isinstance(gb.SAMPLE_DATA,pd.DataFrame))
        
        self.fail("Finish the test!")
    
if __name__ == '__main__':
    unittest.main()
    