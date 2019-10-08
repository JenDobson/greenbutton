"""Parse GreenButton XML (within zipfile)"""

import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os 

import pdb


package_directory = os.path.dirname(os.path.abspath(__file__))

INTERVAL = "./content/IntervalBlock/IntervalReading"
XMLFILE = os.path.join(package_directory, 'sample_data', 'SDGEElectricIntervalDataFeb12011toJan312012.xml')

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
    
    
tree = ET.parse(XMLFILE)
root = tree.getroot()

interval_blocks = get_interval_blocks(root)

readings = []

for interval_block in interval_blocks:
    for interval_reading in get_interval_readings(interval_block):
        readings.append(parse_reading(interval_reading))
 
df = pd.DataFrame(readings,columns=['Start Time','Duration','Watts'])

print(df)

df_night_use = filter_by_time_of_day(df,datetime.time(23,0),datetime.time(5,0))


# Plot use per night 11pm to 5am
df_night_use_by_day = df_night_use.groupby(lambda x: df_night_use['Start Time'].loc[x].date()).sum()
