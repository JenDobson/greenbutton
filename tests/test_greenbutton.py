import unittest
from unittest.mock import patch
import greenbutton.greenbutton as gb

import pandas as pd
import numpy as np
import datetime
import os

THISDIR = os.path.dirname(os.path.abspath(__file__))

class TestStringMethods(unittest.TestCase):
    
    def test_has_sample_data(self):
        self.assertTrue(isinstance(gb.SAMPLE_DATA,pd.DataFrame))
        
    def test_create_box_plot_of_use_by_hour(self):
        ax = gb.boxplot_use_by_hour(gb.SAMPLE_DATA)
        self.assertIsNotNone(ax)
        self.assertNotIn('Start Hour',gb.SAMPLE_DATA.columns)
        self.assertEqual(168,len(ax.lines))
    
    def test_filter_by_time_of_day(self):
        test_df = gb.SAMPLE_DATA.copy()
        filtered_df = gb.filter_by_time_of_day(test_df,datetime.time(8,0,0),datetime.time(9,0,0)) 
        unique_filtered_df = filtered_df['Start Time'].dt.time.unique()
        self.assertTrue(np.isin(datetime.time(8,0),unique_filtered_df))
        self.assertTrue(np.isin(datetime.time(9,0),unique_filtered_df))
        self.assertTrue(2,len(unique_filtered_df))
    
    def test_can_load_data_from_file(self):
        # Check that loaded data is not just from hardcoded XMLFILE
        datafile = os.path.join(THISDIR,'data','testdata.xml')
        df = gb.dataframe_from_xml(datafile)
        self.assertEqual(pd.Timestamp(2019,10,1,0),df.loc[0]['Start Time'])
        
    def test_aggregate_use_by_day(self):
        pass
        
    def test_sample_data_is_immutable(self):
        # see: https://stackoverflow.com/questions/24928306/pandas-immutable-dataframe
        pass
    
if __name__ == '__main__':
    unittest.main()
    