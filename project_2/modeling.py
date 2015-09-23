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

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
DATA_DIR = os.path.abspath(os.path.join('data'))
HOSPITAL_DIR = os.path.join(DATA_DIR, 'heart_disease')
#HOSPITAL_DIR='C:\Users\SKH469\capitalone-pilottwo\project_2\data\heart_disease'

hospital_data=pd.DataFrame()
file_contents = os.listdir(HOSPITAL_DIR)
for filename in file_contents:
    filepath = os.path.join(HOSPITAL_DIR, filename)
    if filepath.endswith('.data'):
        with open(filepath, 'r') as infile:
            hospital_data=hospital_data.append(pd.read_csv(infile, header=None, na_values=['?'], sep=r"[\s,]"))

hospital_data = hospital_data.dropna()
X = hospital_data.iloc[:,:13]
Y = hospital_data.iloc[:,13]

def k_value_test(X,Y,krange,metriclist,numfolds):
    '''
    Solution to first few challenges. Creates a function and pulls most things the different types of metrics
    and the paramter values into loops
    X: n-by-p dataframe of features
    Y: n-by-1 dataframe of target
    krange: List of values of the k parameter for KNN
    metriclist: List of performance metrics. Each element of the list must be valid scoring parameter values.
    numfolds: Number of folds in the cross-validation
    '''
    results_df=pd.DataFrame()
    "====== K-value testing report ======"
    for metric in metriclist:
        resultslist= []
        for k in krange:
            x = KNeighborsClassifier(k)
            results = cross_val_score(x, X, Y, cv=numfolds, scoring=metric)
            resultslist.append((k, results.mean()))
        top_metric = sorted(resultslist, key=lambda p: p[1], reverse=True)
        print "Best K for %s: %i (%f)" % (metric,top_metric[0][0], top_metric[0][1])
        if results_df.shape == (0,0):
            results_df = pd.DataFrame(resultslist, columns=['k',str(metric)])
        else:
            results_df=results_df.merge(pd.DataFrame(resultslist, columns=['k',str(metric)]),on='k')
        #print pd.concat([results_df, pd.DataFrame(resultslist, columns=['k',str(metric)])])
        #print results_df
    results_df.plot(x='k')
    plt.show()
    print results_df

k_value_test(X,Y,range(1,11),['f1_weighted','accuracy','precision_weighted','recall_weighted',None])

def k_value_test2(X,Y,krange,metriclist,numfolds):
    '''
    This function attempts to optimize runtime by only fitting the model once per fold for each parameter level.
    X: n-by-p dataframe of features
    Y: n-by-1 dataframe of target
    krange: List of values of the k parameter for KNN
    metriclist: List of performance metrics. Each element of the list must be score function taking y_true and y_pred as arguments.
    numfolds: number of cross-validation folds    
    '''
    results_df=pd.DataFrame()
    "====== K-value testing report ======"
    for k in krange:
        metric_folds=[]
        for train, test in KFold(Y.shape[0],numfolds):
            X_train, Y_train, X_test, Y_test = np.array(X)[train], np.array(Y)[train], np.array(X)[test], np.array(Y)[test]
            model = KNeighborsClassifier(k)
            model.fit(X_train, Y_train)
            Y_predicted=model.predict(X_test)
            fold_row=[]
            for metric in metriclist:
                fold_row.append(metric(Y_test,Y_predicted))
            metric_folds.append(fold_row)
        results_df=results_df.append(pd.DataFrame.transpose(pd.DataFrame(pd.DataFrame(metric_folds).mean(axis=0))))
    results_df['k']=pd.Series(krange,index=results_df.index)
    results_df.columns=[metric.__name__ for metric in metriclist]+['k']
    results_df.plot(x='k')
    plt.show()
    
    metricnames=results_df.idxmax(axis=0).index
    optparams = [krange[x] for x in results_df.idxmax(axis=0)]
    for i in range(len(metricnames)-1):
        print "Best K for %s: %i (%f)" % (metricnames[i],optparams[i],results_df[metricnames[i]][results_df.idxmax(axis=0)[i]])
    
k_value_test2(X,Y,range(1,11),[metrics.f1_score, metrics.recall_score, metrics.precision_score, metrics.accuracy_score],4)

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
            model = KNeighborsClassifier(k)
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
    
k_value_test3(KNeighborsClassifier,X,Y,range(1,11),[metrics.f1_score, metrics.recall_score, metrics.precision_score, metrics.accuracy_score],4)
