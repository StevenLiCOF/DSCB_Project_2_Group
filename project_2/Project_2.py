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
           files_dict[os.path.splitext(filename)[0][10:]]=pd.read_csv(infile, header=None, index_col=False, na_values=['?'], sep=r"[\s,]")
           
processed_data=pd.DataFrame()
for item in files_dict.keys():
    files_dict[item].columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
    files_dict[item]['location']=item
    processed_data=processed_data.append(files_dict[item])

summaries_dict={}
for item in files_dict.keys():
    summaries_dict[item]=files_dict[item].describe()

del processed_data['ca']

cleveland_data=files_dict['cleveland'].dropna()
X = cleveland_data.iloc[:,:13]
Y = cleveland_data.iloc[:,13]

from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import numpy as np
def k_value_test3(modeltype, X,Y,paramrange,metriclist,numfolds):
    '''
    This is the final function that does everything in the challenge.
    modeltype: Type of model (e.g. KNN), which takes a single parameter argument
    X: n-by-p dataframe of features
    Y: n-by-1 dataframe of target
    paramrange: List of values of the parameter
    metriclist: List of performance metrics. Each element of the list must be score function taking y_true and y_pred as arguments.
    numfolds: number of cross-validation folds
    '''
    results_df=pd.DataFrame()
    "====== K-value testing report ======"
    for k in paramrange:
        metric_folds=[]
        for train, test in KFold(Y.shape[0],numfolds):
            X_train, Y_train, X_test, Y_test = np.array(X)[train], np.array(Y)[train], np.array(X)[test], np.array(Y)[test]
            model = linear_model.Lasso(alpha = k, normalize=True)
            model.fit(X_train, Y_train)
            Y_predicted=model.predict(X_test)
            fold_row=[]
            for metric in metriclist:
                fold_row.append(metric(Y_test,Y_predicted))
            metric_folds.append(fold_row)
        results_df=results_df.append(pd.DataFrame.transpose(pd.DataFrame(pd.DataFrame(metric_folds).mean(axis=0))), ignore_index=True)
    results_df['k']=pd.Series(paramrange,index=results_df.index)
    results_df.columns=[metric.__name__ for metric in metriclist]+['k']
    results_df.plot(x='k')
    plt.show()
    
    metricnames=results_df.idxmax(axis=0).index
    optparams = [paramrange[x] for x in results_df.idxmax(axis=0)]
    for i in range(len(metricnames)-1):
        print "Best K for %s: %i (%f)" % (metricnames[i],optparams[i],results_df[metricnames[i]][results_df.idxmax(axis=0)[i]])
    
k_value_test3(linear_model.Lasso,X,Y,np.arange(0,.01,0.001),[mean_squared_error],4)


#Thal is mostly normal for Cleveland, and mostly defect when not missing for other locations.
#Thus we assume that missing thal means normal for other locations.
#processed_data['thal']=processed_data['thal'].fillna(3)
#processed_data['fbs']=processed_data['fbs'].fillna(3)
#processed_data['slope']=processed_data['slope'].fillna(3)
#processed_data=processed_data.dropna()
#
##Converting target to binary - heart disease or none
#processed_data['num']=processed_data['num'].replace([2,3,4],[1,1,1])
#
##Converting thal to binary - normal or defect
#processed_data['thal']=processed_data['thal'].replace([3,6,7],[0,1,1])
#
#print processed_data[['num','age']].groupby(['num']).mean()
#print processed_data[['num','trestbps']].groupby(['num']).mean()
#
#
#print processed_data[['num','age']].groupby(['age']).mean()
#
#import matplotlib.pyplot as plt
#plt.plot(processed_data['age'], processed_data['num'], 'o')