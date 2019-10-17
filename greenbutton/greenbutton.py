"""Parse GreenButton XML (within zipfile)"""

import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 

import pdb


package_directory = os.path.dirname(os.path.abspath(__file__))

INTERVAL = "./content/IntervalBlock/IntervalReading"
XMLFILE = os.path.join(package_directory, 'sample_data', 'sample_data.xml')

ns = {'default': 'http://www.w3.org/2005/Atom',
    'reading': 'http://naesb.org/espi'}
    
def usage_point():
    tree = ET.parse(XMLFILE)
    root = tree.getroot()
    
    return root.findall('default:entry/default:content/reading:UsagePoint',ns)
    
def start_date_from_interval_block(interval_block_node):
    """ Return start date as DATETIME from interval block xml node """
    start_date_node = interval_block_node.find('reading:interval/reading:start',ns)
    return datetime.datetime.utcfromtimestamp(int(start_date_node.text))
    
def end_date_from_interval_block(interval_block_node):
    """ Return end date as DATETIME from interval block xml node """
    start_date = start_date_from_interval_block(interval_block_node)
    duration_text = interval_block_node.find('reading:interval/reading:duration',ns).text
    duration = datetime.timedelta(seconds=duration_text)
    return start_date + duration
    
def get_interval_blocks(root):
    """ Return list of interval blocks """
    return root.findall('default:entry/default:content/reading:IntervalBlock',ns)
     
def get_interval_readings(interval_block):
    """ Return list of interval readings """
    return interval_block.findall('reading:IntervalReading',ns)

def parse_reading(interval_reading_node):
    start = datetime.datetime.utcfromtimestamp(int(interval_reading_node.find('reading:timePeriod/reading:start',ns).text))
    duration = datetime.timedelta(seconds = int(interval_reading_node.find('reading:timePeriod/reading:duration',ns).text))
    value = int(interval_reading_node.find('reading:value',ns).text)
    return (start, duration, value)
    
def filter_by_time_of_day(df,starttime, stoptime):
    if stoptime < starttime:
        df2 = df[df['Start Time'].map(lambda x: x.time() >= starttime) | df['Start Time'].map(lambda x: x.time() <= stoptime)]
    else:
        df2 = df[df['Start Time'].map(lambda x: x.time() >= starttime) & df['Start Time'].map(lambda x: x.time() <= stoptime)]
    return df2
    
# From https://stackoverflow.com/questions/13108635/how-to-get-time-of-day-for-each-element-in-a-datetime64-array
def start_day(start_time):
    return start_time.astype('datetime64[D]').astype(start_time.dtype)
    
def start_hour(start_time,start_day):
    return (start_time-start_day)/np.timedelta64(1,'h')

def start_time_from_df(df):
    return df['Start Time']

def start_hour_from_df(df):
    start_time = start_time_from_df(df)
    start_day = start_day_from_df(df)
    return np.floor(start_hour(start_time,start_day))
    
def start_day_from_df(df):
    start_time = start_time_from_df(df)
    return start_day(start_time)

def watts_by_use_hour(df):
    return pd.Series(df['Watts'],start_hour_from_df(df))
    
def group_by_use_hour_from_df(df):    
    s = watts_by_use_hour(df)
    return s.groupby(level=0)
    
def boxplot_use_by_hour(df):
    df_to_plot = df.copy()
    df_to_plot['Start Hour'] = start_hour_from_df(df)
    return df_to_plot.boxplot('Wh','Start Hour')
    
    
def dataframe_from_xml(xmlfile):
    tree = ET.parse(XMLFILE)
    root = tree.getroot()

    interval_blocks = get_interval_blocks(root)

    readings = []

    for interval_block in interval_blocks:
        for interval_reading in get_interval_readings(interval_block):
            readings.append(parse_reading(interval_reading))
 
    return pd.DataFrame(readings,columns=['Start Time','Duration','Wh'])
    



SAMPLE_DATA = dataframe_from_xml(XMLFILE)

