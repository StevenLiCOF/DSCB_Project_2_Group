# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:28:47 2015

@author: TXM643
"""
import pandas as pd
#import data
def data_score(actual, predict):
    '''
    actual & predict are lists of values
    '''

    score1 = 0.
    score2 = 0.
    counter = 0
    for item in actual:
        if item != predict[counter]:
            if int(item) > 0 and predict[counter] == 0:
                score1 += 1
            if int(item) == 0 and predict[counter] > 0:
                score2 += 1
        counter +=1
    score_false_0 = score1 / counter
    score_false_1 = score2 / counter
    scores = [score_false_0, score_false_1, 1 - (score_false_0 + score_false_1)]
    print scores
    return scores

if __name__ == "__main__":
    # a Test case
    data_in = pd.DataFrame()
    data_in['actual'] = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,3,4,4]
    data_in['predict'] = [0,0,0,0,0,0,0,0,0,1,0,0,1,1,2,2,3,3,4,4]
    print data_score(data_in['actual'], data_in['predict'])