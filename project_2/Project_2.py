# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:42:06 2015

@author: skh469
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import KFold
from sklearn import metrics
import re

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# constants

#CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
#DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
#DATA_DIR = os.path.abspath(os.path.join('data'))
#HOSPITAL_DIR = os.path.join(DATA_DIR, 'heart_disease')
HOSPITAL_DIR='C:\Users\SKH469\capitalone-pilottwo\project_2\data\heart_disease'

file_contents = os.listdir(HOSPITAL_DIR)
files_dict={}
for filename in file_contents:
    filepath = os.path.join(HOSPITAL_DIR, filename)
    if filepath.endswith('.data') and filename.startswith('processed'):
        with open(filepath, 'r') as infile:
           files_dict[os.path.splitext(filename)[0]]=pd.read_csv(infile, header=None, index_col=False, na_values=['?'], sep=r"[\s,]")

processed_data=pd.DataFrame()
for item in files_dict.keys():
    files_dict[item].columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
    #temp_df.columns = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
    files_dict[item]['location']=item[10:]
    processed_data=processed_data.append(files_dict[item])


for item in files_dict.keys():
    for var in files_dict[item].columns:
        files_dict[item].myvar.value_counts().sort_index() 
        files_dict[item].myvar.value_counts() 
        files_dict[item].myvar.value_counts(dropna=False) 
        files_dict[item].myvar.describe() 
        files_dict[item].myvar.describe(percentiles=[.01, .05, .1, .25, .5, .75, .9, .95, .99])