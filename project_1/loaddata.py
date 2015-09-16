"""loaddata is a module for accessing scraped data about movies from
BoxOfficeMojo and Metacritic.
It's built specifically to work with the data collected for the
CapitalOne Metis Data Science Python Bootcamp Pilot Extravaganza 2K15.
"""

# imports
import os
import json
import pprint
from datetime import datetime

# constants
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
MOJO_DIR = os.path.join(DATA_DIR, 'boxofficemojo')
METACRITIC_DIR = os.path.join(DATA_DIR, 'metacritic')

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
        if type(movie_data)=='dict':
            movie_list.append(movie_data)
    print "Parsed %i movies from %i files" % (len(movie_list),
                                              len(file_contents))
    return movie_list

def load_and_merge_movies():
    mojomovies=get_movies(MOJO_DIR)
    metacriticmovies=get_movies(METACRITIC_DIR)
    for movie in mojomovies:
        if movie['release_date_limited']:
            movie['release_date_limited']=datetime.strptime(movie['release_date_limited'],'%Y-%m-%d').date()
        if movie['release_date_wide']:
            movie['release_date_wide']=datetime.strptime(movie['release_date_wide'],'%Y-%m-%d').date()
    output_dict={}
    for mojomovie in mojomovies:
        for metamovie in metacriticmovies:
            if mojomovie['title'] == metamovie['title']:
                entry=mojomovie
                entry.update(metamovie)
                output_dict.append(entry)

if __name__=="__main__":
    load_and_merge_movies()
