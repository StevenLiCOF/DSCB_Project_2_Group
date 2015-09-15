"""loaddata is a module for accessing scraped data about movies from
BoxOfficeMojo and Metacritic.
It's built specifically to work with the data collected for the
CapitalOne Metis Data Science Python Bootcamp Pilot Extravaganza 2K15.
"""

# imports
import os
import json
import pprint
import datetime

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
        movie_list.append(movie_data)
    print "Parsed %i movies from %i files" % (len(movie_list),
                                              len(file_contents))
    return movie_list

def convert_date(field):
    year=int(field[:4])
    month=int(field[5:7])
    day=int(field[8:10])
    formatteddate=datetime.date(year,month,day)
    return formatteddate

def merge_lists(l1, l2, key):
    merged = {}
    for item in l1+l2:
        if item[key] in merged:
            merged[item[key]].update(item)
        else:
            merged[item[key]] = item
    return [val for (_, val) in merged.items()]

def load_and_merge_movies():
    mojomovies=get_movies(MOJO_DIR)
    metacriticmovies=get_movies(METACRITIC_DIR)
    for movie in mojomovies:
        movie['release_date_limited']=convert_date(movie['release_date_limited'])
        movie['release_date_wide']=convert_date(movie['release_date_wide'])
    union=merge_lists(mojomovies,metacriticmovies,'title')
    intersection=[]
    for movie in union:
        if movie['title'] in list(set([mojomovie['title'] for mojomovie in mojomovies]) &
                                  set([metacriticmovie['title'] for metacriticmovie in metacriticmovies])):
            intersection.append(movie)
    return intersection


if __name__=="__main__":
    load_and_merge_movies()
