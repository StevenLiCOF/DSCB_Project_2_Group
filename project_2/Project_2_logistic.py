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
    files_dict[item].columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
                            'exang','oldpeak','slope','ca','thal','num']
    files_dict[item]['location']=item
    processed_data=processed_data.append(files_dict[item])

summaries_dict={}
for item in files_dict.keys():
    summaries_dict[item]=files_dict[item].describe()

#del processed_data['ca']
cleveland_data=files_dict['cleveland'].dropna()
cleveland_data['treated_chol']=cleveland_data['chol'].apply(lambda x: max(x,190))
cleveland_data['low_chol_ind']=cleveland_data['chol'].apply(lambda x: x<190)

features=['age', 'sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang',
 'oldpeak', 'slope', 'ca', 'thal', 'treated_chol', 'low_chol_ind']
X = cleveland_data[features]
Y = cleveland_data['num']
Y=Y.replace([2,3,4],[1,1,1])

from sklearn import linear_model
from sklearn.metrics import mean_squared_error

#Univariate views of input to check for relationship with target
num_avg_groupby_list = ['cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
for var in num_avg_groupby_list: 
    plt.figure() 
    cleveland_data[['num',var]].sort(var).groupby([var])['num'].mean().plot()

#Calibrating lasso parameter
from pprint import pprint
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
            model = modeltype(penalty='l1', C = k)
            model.fit(X_train, Y_train)
            #pprint(zip(X.columns.values,model.coef_))
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
    
    metricnames=results_df.idxmin(axis=0).index
    optparams = [paramrange[x] for x in results_df.idxmin(axis=0)]
    for i in range(len(metricnames)-1):
        print "Best K for %s: %f (%f)" % (metricnames[i],optparams[i],results_df[metricnames[i]][results_df.idxmin(axis=0)[i]])
    
k_value_test3(linear_model.LogisticRegression,X,Y,np.arange(1.0,4.0,0.05),[mean_squared_error],4)

#Fit lasso model
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
lassomodel=linear_model.Lasso(alpha = 0.004, normalize=True)
lassomodel.fit(X_train, Y_train)
Y_test=pd.DataFrame(Y_test)
Y_test['prediction']=lassomodel.predict(X_test)
Y_test['num_capped']=Y_test['num'].replace([2,3,4],[1,1,1])
#Print model coefficients
pprint(zip(X.columns.values,lassomodel.coef_))
print mean_squared_error(Y_test['num'],Y_test['prediction'])
#print lassomodel.intercept_
#Age and cholesterol were selected out of the model.
#Since this is unintuitive, we plot both against some other predictors to see if they are closely correlated.
plt.scatter(cleveland_data['age'],cleveland_data['trestbps'])
plt.scatter(cleveland_data['chol'],cleveland_data['trestbps'])
plt.scatter(cleveland_data['age'],cleveland_data['thalach'])
plt.scatter(cleveland_data['chol'],cleveland_data['thalach'])

#Univariate views of cholesterol and age
cleveland_data['agebin']=pd.DataFrame(pd.qcut(cleveland_data['age'], 10))
plt.figure() 
ax = cleveland_data[['num','agebin']].sort('agebin').groupby(['agebin'])['num'].mean().plot()
for tick in ax.get_xticklabels():
        tick.set_rotation(45)

cleveland_data['cholbin']=pd.DataFrame(pd.qcut(cleveland_data['chol'], 10))
plt.figure() 
ax=cleveland_data[['num','cholbin']].sort('cholbin').groupby(['cholbin'])['num'].mean().plot()
for tick in ax.get_xticklabels():
        tick.set_rotation(45)

import seaborn
with seaborn.axes_style('white'):
    Y_test.boxplot(column='prediction',by='num')
    seaborn.despine()
# Compute ROC curve and ROC area for each class
fpr, tpr, _ = metrics.roc_curve(Y_test['num_capped'], Y_test['prediction'])
roc_auc = metrics.auc(fpr, tpr)
# Plot of a ROC curve for a specific class
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

metrics_summary=[]
for threshold in np.arange(0,2,0.1):
    def custom_round(x):
        if x>threshold:
            return 1
        else:
            return 0
    print [threshold,
           metrics.accuracy_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
           metrics.precision_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
           metrics.recall_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
           metrics.f1_score(Y_test['num_capped'],map(custom_round,Y_test['prediction']))]
    metrics_summary.append([threshold,
            metrics.accuracy_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
            metrics.precision_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
            metrics.recall_score(Y_test['num_capped'],map(custom_round,Y_test['prediction'])),
            metrics.f1_score(Y_test['num_capped'],map(custom_round,Y_test['prediction']))])
metrics_summary=pd.DataFrame(metrics_summary)
metrics_summary.columns=['threshold','accuracy','precision','recall','f1']
plt.figure()
plt.plot(metrics_summary['threshold'],metrics_summary[['accuracy','precision','recall','f1']])
plt.xlabel('Heart Disease Threshold')
plt.ylabel('Classification Metric')
plt.legend(metrics_summary.columns[1:],loc='best')
            
