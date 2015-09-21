# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:09:05 2015

@author: skh469
"""

#Challenge 1
import pandas as pd
import numpy as np

vote_data = pd.read_csv('C:\Users\skh469\capitalone-pilottwo\day_06\house-votes-84.csv', header=None)

vote_data=vote_data.replace('y',1).replace('n',0)
isnum = vote_data.applymap(np.isreal)

for i in range(16):
    mean=vote_data[i+1][isnum[i+1]==True].mean()
    vote_data[i+1]=vote_data[i+1].replace('?',mean)
    
#Challenge 2
from sklearn.cross_validation import train_test_split
vote_train, vote_test = train_test_split(vote_data, test_size=0.2, random_state=11)

#Challenge 3
from sklearn.neighbors import KNeighborsClassifier
#Awesome name for a dataframe
party_train=vote_train[0]
party_test=vote_test[0]
votes_train=pd.DataFrame(vote_train,columns=list(range(1,17)))
votes_test=pd.DataFrame(vote_test,columns=list(range(1,17)))

from sklearn.metrics import accuracy_score

for k in range(1,21):
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(votes_train,party_train)
    party_predicted_knn=knn_model.predict(votes_test)
    print (k, accuracy_score(party_test, party_predicted_knn))

#Challenge 4
from sklearn.linear_model import LogisticRegression
logit_model = LogisticRegression()
logit_model.fit(votes_train,party_train)
party_predicted_logit=logit_model.predict(votes_test)
accuracy_score(party_test,party_predicted_logit)

#Challenge 5
import matplotlib.pyplot as plt
import seaborn

parties_agg=vote_data[[0,1]].groupby([0]).count()

with seaborn.axes_style('white'):
    plot=parties_agg.plot(kind='bar')

print 'There are %s Democrats and %s Republicans' % (parties_agg.iloc[0,0],parties_agg.iloc[1,0])

def all_reps(inarray):
    return np.array(['republican']*inarray.shape[0])
def all_dems(inarray):
    return np.array(['democrat']*inarray.shape[0])
    
party_predicted_allreps = all_reps(votes_test)
party_predicted_alldems = all_dems(votes_test)
    
accuracy_score(party_test,party_predicted_allreps)
accuracy_score(party_test,party_predicted_alldems)

#Chalenge 6
perf_array=[]

logit_model = LogisticRegression()
logit_model.fit(votes_train,party_train)
party_predicted_logit=logit_model.predict(votes_test)
accuracy_score_logit=accuracy_score(party_test,party_predicted_logit)

accuracy_score_allreps=accuracy_score(party_test,party_predicted_allreps)
accuracy_score_alldems=accuracy_score(party_test,party_predicted_alldems)

for k in range(1,300):
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(votes_train,party_train)
    party_predicted_knn=knn_model.predict(votes_test)
    perf_array.append([accuracy_score(party_test, party_predicted_knn),
                       accuracy_score_logit,
                       accuracy_score_allreps,
                       accuracy_score_alldems])

perf_array=pd.DataFrame(perf_array)
perf_array.columns=['KNN','Logit','All Republican','All Democrat']

with seaborn.axes_style('white'):
    plot=perf_array.plot(kind='line')
    seaborn.despine()

#Challenge 7
from sklearn import cross_validation
party_all=vote_data[0]
votes_all=pd.DataFrame(vote_data,columns=list(range(1,17)))
for k in range(1,21):
    knn_model_crossval = KNeighborsClassifier(n_neighbors=k)
    scores = cross_validation.cross_val_score(knn_model_crossval, votes_all, party_all, cv=5)
    print (k, scores.mean())
#The best k is likely to change between holdout and cross-validation when
#either the target is sparse or misclassification is rare, as CV gives a
#broader view of the data as a test sample
    
#Challenge 8
import matplotlib.pyplot as plt   
import matplotlib.pylab as pylab

avgerror=[]
stderror=[]
for k in range(1,21):
    knn_model_crossval = KNeighborsClassifier(n_neighbors=k)
    scores = cross_validation.cross_val_score(knn_model_crossval, votes_all, party_all, cv=5)
    avgerror.append(scores.mean())
    stderror.append(scores.std())

avgerror=np.array(avgerror)
stderror=np.array(stderror)

with seaborn.axes_style('white'):
    plt.errorbar(np.array(range(1,21)),avgerror,yerr=stderror)
    pylab.ylim([0,1])
    seaborn.despine()
    
#Challenge 9
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

print 'All Democrats Model'
print 'Accuracy Score: %s' % accuracy_score(party_test,party_predicted_alldems)
print 'Precision Score (Republican target): %s' % precision_score(party_test,party_predicted_alldems, pos_label='republican', average='binary')
print 'Recall Score (Republican target): %s' % recall_score(party_test,party_predicted_alldems, pos_label='republican', average='binary')
print 'F1 Score (Republican target): %s' % f1_score(party_test,party_predicted_alldems, pos_label='republican', average='binary')
print ''
print 'All Republicans Model'
print 'Accuracy Score: %s' % accuracy_score(party_test,party_predicted_allreps)
print 'Precision Score (Republican target): %s' % precision_score(party_test,party_predicted_allreps, pos_label='republican', average='binary')
print 'Recall Score (Republican target): %s' % recall_score(party_test,party_predicted_allreps, pos_label='republican', average='binary')
print 'F1 Score (Republican target): %s' % f1_score(party_test,party_predicted_allreps, pos_label='republican', average='binary')
print ''
print 'Logistic Regression Model'
print 'Accuracy Score: %s' % accuracy_score(party_test,party_predicted_logit)
print 'Precision Score (Republican target): %s' % precision_score(party_test,party_predicted_logit, pos_label='republican', average='binary')
print 'Recall Score (Republican target): %s' % recall_score(party_test,party_predicted_logit, pos_label='republican', average='binary')
print 'F1 Score (Republican target): %s' % f1_score(party_test,party_predicted_logit, pos_label='republican', average='binary')
print ''
print 'K Nearest Neighbors Model'
print 'Accuracy Score: %s' % accuracy_score(party_test,party_predicted_knn)
print 'Precision Score (Republican target): %s' % precision_score(party_test,party_predicted_knn, pos_label='republican', average='binary')
print 'Recall Score (Republican target): %s' % recall_score(party_test,party_predicted_knn, pos_label='republican', average='binary')
print 'F1 Score (Republican target): %s' % f1_score(party_test,party_predicted_knn, pos_label='republican', average='binary')

#Challenge 10
#Note: Should refactor code by defining a function that passes the model as an argument if I have time
from sklearn.cross_validation import KFold
kf = KFold(vote_data.shape[0], n_folds=5)
i=0
AllDemsAcc=[]
AllDemsPrec=[]
AllDemsRecl=[]
AllDemsF1=[]

AllRepsAcc=[]
AllRepsPrec=[]
AllRepsRecl=[]
AllRepsF1=[]

LogitAcc=[]
LogitPrec=[]
LogitRecl=[]
LogitF1=[]

KNNAcc=[]
KNNPrec=[]
KNNRecl=[]
KNNF1=[]

for train, test in kf:
    i+=1
    votes_train, votes_test, party_train, party_test = np.array(votes_all)[train], np.array(votes_all)[test], np.array(party_all)[train], np.array(party_all)[test]
    knn_model = KNeighborsClassifier(n_neighbors=4)
    knn_model.fit(votes_train,party_train)    
    party_predicted_knn=knn_model.predict(votes_test)
    logit_model = LogisticRegression()
    logit_model.fit(votes_train,party_train)
    party_predicted_logit=logit_model.predict(votes_test)
    party_predicted_alldems=all_dems(votes_test)
    party_predicted_allreps=all_reps(votes_test)
    
    AllDemsAcc.append(accuracy_score(party_test,party_predicted_alldems))
    AllDemsPrec.append(precision_score(party_test,party_predicted_alldems, pos_label='republican', average='binary'))
    AllDemsRecl.append(recall_score(party_test,party_predicted_alldems, pos_label='republican', average='binary'))
    AllDemsF1.append(f1_score(party_test,party_predicted_alldems, pos_label='republican', average='binary'))
    
    AllRepsAcc.append(accuracy_score(party_test,party_predicted_allreps))
    AllRepsPrec.append(precision_score(party_test,party_predicted_allreps, pos_label='republican', average='binary'))
    AllRepsRecl.append(recall_score(party_test,party_predicted_allreps, pos_label='republican', average='binary'))
    AllRepsF1.append(f1_score(party_test,party_predicted_allreps, pos_label='republican', average='binary'))    

    LogitAcc.append(accuracy_score(party_test,party_predicted_logit))
    LogitPrec.append(precision_score(party_test,party_predicted_logit, pos_label='republican', average='binary'))
    LogitRecl.append(recall_score(party_test,party_predicted_logit, pos_label='republican', average='binary'))
    LogitF1.append(f1_score(party_test,party_predicted_logit, pos_label='republican', average='binary'))

    KNNAcc.append(accuracy_score(party_test,party_predicted_knn))
    KNNPrec.append(precision_score(party_test,party_predicted_knn, pos_label='republican', average='binary'))
    KNNRecl.append(recall_score(party_test,party_predicted_knn, pos_label='republican', average='binary'))
    KNNF1.append(f1_score(party_test,party_predicted_knn, pos_label='republican', average='binary'))    

print 'All Democrats Model'
print 'Average Accuracy Score: %s' % np.array(AllDemsAcc).mean()
print 'Average Precision Score (Republican target): %s' % np.array(AllDemsPrec).mean()
print 'Average Recall Score (Republican target): %s' % np.array(AllDemsRecl).mean()
print 'Average F1 Score (Republican target): %s' % np.array(AllDemsF1).mean()
print ''
print 'All Republicans Model'
print 'Average Accuracy Score: %s' % np.array(AllRepsAcc).mean()
print 'Average Precision Score (Republican target): %s' % np.array(AllRepsPrec).mean()
print 'Average Recall Score (Republican target): %s' % np.array(AllRepsRecl).mean()
print 'Average F1 Score (Republican target): %s' % np.array(AllRepsF1).mean()
print ''
print 'Logistic Regression Model'
print 'Average Accuracy Score: %s' % np.array(LogitAcc).mean()
print 'Average Precision Score (Republican target): %s' % np.array(LogitPrec).mean()
print 'Average Recall Score (Republican target): %s' % np.array(LogitRecl).mean()
print 'Average F1 Score (Republican target): %s' % np.array(LogitF1).mean()
print ''
print 'K Nearest Neighbors Model'
print 'Average Accuracy Score: %s' % np.array(KNNAcc).mean()
print 'Average Precision Score (Republican target): %s' % np.array(KNNPrec).mean()
print 'Average Recall Score (Republican target): %s' % np.array(KNNRecl).mean()
print 'Average F1 Score (Republican target): %s' % np.array(KNNF1).mean()
print ''