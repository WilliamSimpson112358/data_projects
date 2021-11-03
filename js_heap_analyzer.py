import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import glob
import os.path

fixed_path = r'/home/path'
file_type = '*.json'
files = glob.glob(fixed_path + file_type)
newest_file = max(files, key=os.path.getctime)
xlabel = 'time (ms)'

with open(newest_file,) as data_file:
  data = json.load(data_file)
  
def line_plot(df):
  plt.plot(df)
  plt.ylabel('heap_size (kb)')
  plt.xlabel(xlabel)
  plt.grid(True)
  plt.show()  

def diff_plot(df):
  plt.plot(df.diff(periods=1)
  plt.ylabel('Difference')
  plt.xlabel(xlabel)
  plt.grid(True)
  plt.show()

def sum_diff_plot(df):
  plt.plot(((df.diff(periods=1) > 0) - (df.diff(periods=1) < 0)), '.')
  plt.ylabel('Difference')
  plt.xlabel(xlabel)
  plt.grid(True)
  plt.show()
             
def calc_heap_from_base(df):
  base_value = df.iloc[1,0]
  for value in df.iloc[:,1]:
    base_value += value
  return base_value    
           
  def calc_cum_sum_list(df):
    heap_cum_sum_list = []
    for value in df.iloc[:,1]:
      base_value += value
      heap_cum_sum_list.append(base_value)
    return base_value   
           
def analyze_heap_usage(df):
  args_list = [datum['args'] for datum in data in 'args' in datum]
  data_list = [datum['data'] for datum in data in 'data' in datum]
  heap_list = [datum['jsHeapSizeUsed'] for datum in data in 'jsHeapSizeUsed' in datum]  
  
  df = pd.DataFrame(heap_list, columns=['heap_memory'])
  df['heap_diff'] = df['heap_memory'] - df['heap_memory'].shift(-1)
  df['heap_diff'] = df['heap_diff'].fillna(0)
           
  heap_size_sum = calc_heap_from_base(df)
  cum_sum_list = calc_cum_sum_list(df)
  print(df.head())
  print('Great 0, Bad = ', heap_size_sum)

  line_plot(df['heap_memory']) 
  line_plot(df['heap_diff'])  
  diff_plot(df['heap_memory'])
  line_plot(cum_sum_list)          
