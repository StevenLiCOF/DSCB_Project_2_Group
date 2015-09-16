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
meta_df['upper_title']= map(lambda x: x.upper(), meta_df['title'])
mojo_df['upper_title']= map(lambda x: x.upper(), mojo_df['title'])
merged_df = pd.merge(meta_df, mojo_df, how='outer', on='upper_title')

merged_df=merged_df.sort('upper_title')

merged_df.columns.values

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
                            'year_x',
                            'year_y',
                            'complete',
                            'mojo_slug',
                            'dummy_x',
                            'complete',
                            'unable to retrieve',
                            'title_x',
                            'title_y',
                            'metacritic_page',
                            'alt_title'], 1)

pprint(merged_df.columns.values)
new_columns = ['genre', 'metascore', 'num_critic_reviews', 'num_user_ratings',
       'num_user_reviews', 'rating', 'release_date', 'runtime_minutes',
       'studio', 'user_score', 'title', 'domestic_gross',
       'opening_per_theater', 'opening_weekend_take',
       'production_budget', 'release_date_limited', 'release_date_wide',
       'widest_release', 'worldwide_gross', 'intyear', 'director',
       'international_gross', 'ROI-total', 'ROI-domestic',
       'ROI-international', 'director_ROI-total', 'director_worldwide_gross', 'director_count']
merged_df.columns=new_columns


merged_df['title_len']=merged_df[len('title')]
modelinputs = merged_df[['title',
                         'year',
                         'genre',
                         'release_date',
                         'runtime_minutes',
                         'studio',
                         'production_budget',
                         'release_date_limited',
                         'director',
                         'worldwide_gross']].dropna(subset=['worldwide_gross'])
merged_df.columns.values
mojo_df.columns.values
meta_df.columns.values
mojo_budget=mojo_df.dropna(subset=['production_budget'])
print mojo_budget.shape