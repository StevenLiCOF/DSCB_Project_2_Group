# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 10:40:08 2015

@author: skh469
"""

import os
import json
from pprint import pprint

MOJO_DIR = os.path.join('data','boxofficemojo') 
META_DIR = os.path.join('data','metacritic') 
def get_movies(directory):
    '''Returns a list of dictionaries containing information in the
    JSON files of the provided directory, and prints the number
    of movies read'''
    file_contents = os.listdir(directory)
    movie_list=[]
    for filename in file_contents:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as movie_file:
            movie_data = json.load(movie_file)
        if type(movie_data) == dict:
            movie_list.append(movie_data)
    print "Parsed %i movies from %i files" % (len(movie_list),
                                              len(file_contents))
    return movie_list
mojomovies=get_movies(MOJO_DIR)
metacriticmovies=get_movies(META_DIR)
from datetime import datetime

for movie in mojomovies:
    if movie['release_date_limited']:
        movie['release_date_limited']=datetime.strptime(movie['release_date_limited'],'%Y-%m-%d').date()
    if movie['release_date_wide']:
        movie['release_date_wide']=datetime.strptime(movie['release_date_wide'],'%Y-%m-%d').date()
import numpy as np
import pandas as pd

mojo_df = pd.DataFrame(mojomovies)
meta_df = pd.DataFrame(metacriticmovies)
meta_df['year']=meta_df['year'].replace('',np.nan)
meta_df=meta_df.sort('year')
meta_df=meta_df.dropna(subset=['title','year'],how='any')
mojo_df=mojo_df.dropna(subset=['title','year'],how='any')
meta_df['intyear']=[int(year) for year in meta_df['year']]
mojo_df['intyear']=[int(year) for year in mojo_df['year']]
import re,string
meta_df['char_title']= map(lambda x: re.sub('[\W_]+', '', x).upper(), meta_df['title'])
mojo_df['char_title']= map(lambda x: re.sub('[\W_]+', '', x).upper(), mojo_df['title'])
merged_df = pd.merge(meta_df, mojo_df, how='outer', on='char_title')


merged_df['intyear'] = merged_df['intyear_x'].fillna(merged_df['intyear_y'])

merged_df['director'] = merged_df['director_x'].fillna(merged_df['director_y'])

merged_df['international_gross']=merged_df['worldwide_gross']-merged_df['domestic_gross']
#merged_df['international_gross'].describe()

merged_df['ROI-total']=merged_df['worldwide_gross']/merged_df['production_budget']
merged_df['ROI-domestic']=merged_df['domestic_gross']/merged_df['production_budget']
merged_df['ROI-international']=merged_df['international_gross']/merged_df['production_budget']
merged_df['ROI-total'].describe()
merged_df['ROI-domestic'].describe()
merged_df['ROI-international'].describe()
merged_df['production_budget'].describe()
merged_df=merged_df.sort('ROI-total')

merged_df['dummy']=1
director_money=merged_df[['director','ROI-total','worldwide_gross']].groupby(['director']).mean()
director_count=merged_df[['director','dummy']].groupby(['director']).count()
director_money['director']=director_money.index
director_count['director']=director_count.index
director_merged = pd.merge(director_money, director_count, how='outer', on='director')
merged_df = pd.merge(merged_df, director_merged, how='outer', on='director')

merged_df = merged_df.drop(['director_x',
                            'director_y',
                            'intyear_x',
                            'intyear_y',
                            #'upper_title_x',
                            #'upper_title_y',
                            'year_x',
                            'year_y',
                            'complete',
                            'mojo_slug',
                            'dummy_x',
                            'complete',
                            'unable to retrieve',
                            'metacritic_page',
                            'alt_title'], 1)

pprint(merged_df.columns.values)
new_columns = ['genre', 'metascore', 'num_critic_reviews', 'num_user_ratings',
       'num_user_reviews', 'rating', 'release_date', 'runtime_minutes',
       'studio','title_meta', 'user_score', 'title', 'domestic_gross',
       'opening_per_theater', 'opening_weekend_take',
       'production_budget', 'release_date_limited', 'release_date_wide','title_mojo',
       'widest_release', 'worldwide_gross', 'intyear', 'director',
       'international_gross', 'ROI-total', 'ROI-domestic',
       'ROI-international', 'director_ROI-total', 'director_worldwide_gross', 'director_count']
merged_df.columns=new_columns

#john_carpenter_films=merged_df[merged_df.director == 'John Carpenter']

genres=list(merged_df['genre'].dropna())
genres2=set([item for sublist in genres for item in sublist])

#print len(genres2)

for genre in genres2:
    merged_df[genre]=map(lambda x: (type(x)==list) and (str(genre) in x), merged_df['genre'])

merged_df['title_len']=map(len, merged_df['title'])
merged_df['title_words']=map(lambda x: len(x.split()), merged_df['title'])

merged_df.rating.value_counts()

rating_mapping={
'R':3,
'PG-13':2,
'Not Rated':3,
'PG':1,
'':3,
'nan':3,
'Unrated':3,
'G':0,
'TV-MA':3,
'NC-17':4,
'TV-14':2,
'TV-PG':1,
'TV-G':0,
'Approved':3,
'X':4,
'M':1,
'GP':1,
'PG--13':2,
'Passed':0,
'Open':0,
'TV-Y7':0,
'AO':4
}

merged_df['rating_num']=map(lambda x: rating_mapping[str(x)] ,merged_df['rating'])

merged_df['release_date_yr_mth'] = zip(merged_df['release_date'].str[0:4], merged_df['release_date'].str[5:7])
merged_df['release_date_limited_yr_mth'] = zip(merged_df['release_date_limited'].str[0:4], merged_df['release_date_limited'].str[5:7])
merged_df['release_date_wide_yr_mth'] = zip(merged_df['release_date_wide'].str[0:4], merged_df['release_date_wide'].str[5:7])
merged_df['release_date_mth']=merged_df['release_date'].str[5:7]

dummies=pd.get_dummies(merged_df['release_date_mth'])
merged_df = pd.concat([merged_df,dummies],axis=1)

pprint(merged_df.columns.values)

features=['intyear','runtime_minutes',
       'production_budget',
       'Sci-Fi', 'Crime',
       'Romance', 'Animation', 'Music', 'Adult', 'Comedy', 'War',
       'Horror', 'Film-Noir', 'Western', 'News', 'Thriller',
       'Adventure', 'Mystery', 'Short', 'Drama', 'Action',
       'Documentary', 'Musical', 'History', 'Family', 'Fantasy',
       'Sport', 'Biography', 'title_len', 'title_words', 'rating_num'
       ,'01','02','03','04','05','06','07','08','09','10','11']
related_columns=features+['ROI-total','title','release_date_yr_mth']
clean_data = merged_df[related_columns].dropna()

import statsmodels.api as sm
Y = [np.log(ROI) for ROI in clean_data['ROI-total']]
X = clean_data[features]

from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

from sklearn import linear_model
from sklearn.metrics import mean_squared_error
def runlasso(setalpha):
    clf = linear_model.Lasso(alpha = setalpha, normalize=True)
    clf.fit(X_train,Y_train)
    Y_predicted = clf.predict(X_test)
    print (mean_squared_error(Y_predicted, Y_test),setalpha)
    #print clf.coef_
    #print clf.intercept_
    return clf
for i in np.arange(0,0.002,0.0001):
    model = runlasso(i)
print model.coef_

clf = linear_model.Lasso(alpha = .0005, normalize=True)
clf.fit(X_train,Y_train)
print clf.coef_
print clf.intercept_
Y_predicted = clf.predict(X_test)
print mean_squared_error(Y_predicted, Y_test)

coeffs = zip(X_test.columns.values,clf.coef_)

import matplotlib
import seaborn

predvsact = pd.DataFrame(zip(Y_predicted, Y_test))
predvsact.columns=['predicted','actual']


    
clean_data['predicted_log(ROI)'] = clf.predict(clean_data[features])
clean_data['log(ROI)'] = [np.log(value) for value in clean_data['ROI-total']]
clean_data['resid'] = clean_data['log(ROI)']-clean_data['predicted_log(ROI)']

import matplotlib.pyplot as plt
with seaborn.axes_style('white'):
    plot = clean_data.plot(kind='scatter', 
                      x='predicted_log(ROI)', 
                      y='log(ROI)', 
                      alpha=0.5,
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("How well does our model predict ROI?")
    plot.set_xlim([-1,5])
    plot.set_ylim([-1,5])
    plot.set_xlabel('predicted_log(ROI)')
    plot.set_ylabel('log(ROI)')
    plt.plot(clean_data['log(ROI)'], clean_data['log(ROI)'], 'r')
    
with seaborn.axes_style('white'):
    plot = clean_data.plot(kind='scatter', 
                      x='predicted_log(ROI)', 
                      y='resid', 
                      alpha=0.5,
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("Residuals by prediction")
    plot.set_xlim([-1,3])
    plot.set_ylim([-7,9])
    plot.set_xlabel('predicted_log(ROI)')
    plot.set_ylabel('resid')
    #plt.plot(clean_data['log(ROI)'], clean_data['log(ROI)'], 'r')
    
modelperf_year=clean_data[['intyear','predicted_log(ROI)','log(ROI)']].groupby(['intyear']).mean()

with seaborn.axes_style('white'):
    plot = modelperf_year.plot(kind='line', 
                      #x='intyear', 
                      y=['log(ROI)', 'predicted_log(ROI)'],
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("ROI predicted vs. actual by year")
    plot.set_xlim([1995,2015])
    plot.set_ylim([0,2])
    plot.set_xlabel('Year')
    plot.set_ylabel('ROI')
    #plt.plot(clean_data['ROI-total'], clean_data['ROI-total'], 'r')



ur_df = pd.read_csv(os.path.join('historical_unemp_rate.csv'), index_col = 'Year')

#ur_df = pd.read_csv('C:\Users\dxk277\Desktop\Project\python\DSBC_Project1_Group3\historical_unemp_rate.csv', index_col = 'Year')

ur_df = ur_df.stack()

ur_dic = dict(ur_df)

type(ur_dic.keys()[0])

ds_df = pd.read_csv(os.path.join('USDollarIndexTable.csv'), index_col = 'DATE')

#ds_df = pd.read_csv('C:\Users\dxk277\Desktop\Project\python\DSBC_Project1_Group3\USDollarIndexTable.csv', index_col = 'DATE')
ds_dic = dict(ds_df.stack())

list_keys = [item[0] for item in ds_dic.keys()]

def get_ds_year(strings):   
    year = strings[4:]
    if int(year) <20:
        year = '20'+year
    else:
        year = '19'+year
    return year

def get_ds_month(strings):
    month = strings[:3]
    if month == 'Jan': 
        month = '01'
    elif month == 'Feb': 
        month = '02'
    elif month == 'Mar': 
        month = '03'
    elif month == 'Apr': 
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun':
        month = '06'
    elif month == 'Jul':
        month = '07'
    elif month == 'Aug':
        month = '08'
    elif month == 'Sep':
        month = '09'
    elif month == 'Oct':
        month = '10'
    elif month == 'Nov':
        month = '11'
    elif month == 'Dec':
        month = '12'
    return month

list_new_keys = [(get_ds_year(key), get_ds_month(key)) for key in list_keys]

list_values = [item for item in ds_dic.values()]

ds_dic_new = dict(zip(list_new_keys,list_values))

list_ur_keys = [item for item in ur_dic.keys()]

def get_ur_year(list_of_keys):
    year = str(list_of_keys[0])
    return year

def get_ur_month(list_of_keys):
    month = str(list_of_keys[1])
    if month == 'Jan': 
        month = '01'
    elif month == 'Feb': 
        month = '02'
    elif month == 'Mar': 
        month = '03'
    elif month == 'Apr': 
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun':
        month = '06'
    elif month == 'Jul':
        month = '07'
    elif month == 'Aug':
        month = '08'
    elif month == 'Sep':
        month = '09'
    elif month == 'Oct':
        month = '10'
    elif month == 'Nov':
        month = '11'
    elif month == 'Dec':
        month = '12'
    return month
    
list_new_ur_keys = [(get_ur_year(key), get_ur_month(key)) for key in list_ur_keys]

list_ur_values = [item for item in ur_dic.values()]

ur_dic_new = dict(zip(list_new_ur_keys,list_ur_values))

merged_df['dollar_index'] = [ds_dic_new.get(merged_df['release_date_yr_mth'][i]) for i in range(len(merged_df['release_date_yr_mth']))]

merged_df['unemployment_rate'] = [ur_dic_new.get(merged_df['release_date_yr_mth'][i]) for i in range(len(merged_df['release_date_yr_mth']))]

keepcols=['ROI-total','domestic_gross','worldwide_gross','intyear','dollar_index','unemployment_rate','release_date_yr_mth']
clean_data2=merged_df[keepcols].dropna()

clean_data2['domestic_gross_ratio'] = clean_data2['domestic_gross']/clean_data2['worldwide_gross']


with seaborn.axes_style('white'):
    plot = clean_data2.plot(kind='scatter', 
                      x='dollar_index', 
                      y='domestic_gross_ratio', 
                      alpha=0.5,
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("Domestic Gross Ratio against Dollar Strength")
    plot.set_xlim([80,140])
    plot.set_ylim([0,1])
    plot.set_xlabel('dollar_index')
    plot.set_ylabel('domestic_gross_ratio')
    #plt.plot(clean_data['log(ROI)'], clean_data['log(ROI)'], 'r')
    
with seaborn.axes_style('white'):
    plot = clean_data2.plot(kind='scatter', 
                      x='unemployment_rate', 
                      y='domestic_gross', 
                      alpha=0.5,
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("Domestic Gross against Unemployment")
    plot.set_xlim([3,11])
    plot.set_ylim([0,800000000])
    plot.set_xlabel('unemployment_rate')
    plot.set_ylabel('domestic_gross')
    #plt.plot(clean_data['log(ROI)'], clean_data['log(ROI)'], 'r')
    
    
clean_data2['domestic_gross_normalized']=clean_data2['domestic_gross']/800000000
clean_data2['unemployment_rate_normalized']=clean_data2['unemployment_rate']/20
clean_data2['dollar_index_normalized']=clean_data2['dollar_index']/200
econ_year=clean_data2[['intyear','domestic_gross_ratio','unemployment_rate_normalized','domestic_gross_normalized','dollar_index_normalized']].groupby(['intyear']).mean()
#with seaborn.axes_style('white'):
#    plot = econ_year.plot(kind='line', 
#                      #x='unemployment_rate', 
#                      y=['domestic_gross_normalized','unemployment_rate_normalized'],
#                      figsize=(10,6))
#    seaborn.despine()
#    plot.set_title("Domestic Gross against Unemployment")
#    plot.set_ylim([0,1])
with seaborn.axes_style('white'):
    plot = econ_year.plot(kind='line', 
                      #x='unemployment_rate', 
                      y=['domestic_gross_ratio','dollar_index_normalized','unemployment_rate_normalized'],
                      #alpha=0.5,
                      figsize=(10,6))
    seaborn.despine()
    plot.set_title("Domestic Gross against Unemployment")
    #plot.set_xlim([3,11])
    plot.set_ylim([0,0.7])
    #plot.set_xlabel('unemployment_rate')
    #plot.set_ylabel('domestic_gross')
merged_df[['Sci-Fi', 'Crime',
       'Romance', 'Animation', 'Music', 'Adult', 'Comedy', 'War',
       'Horror', 'Film-Noir', 'Western', 'News', 'Thriller',
       'Adventure', 'Mystery', 'Short', 'Drama', 'Action',
       'Documentary', 'Musical', 'History', 'Family', 'Fantasy',
       'Sport', 'Biography']].sum()

clf.score(X,Y)