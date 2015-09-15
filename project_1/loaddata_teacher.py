"""loaddata is a module for accessing scraped data about movies from
BoxOfficeMojo and Metacritic.
It's built specifically to work with the data collected for the
CapitalOne Metis Data Science Python Bootcamp Pilot Extravaganza 2K15.
"""

# imports
import os
import sys
import json
import datetime
from pprint import pprint

# constants
DATA_DIR = os.path.abspath('data')
MOJO_DIR = os.path.join(DATA_DIR, 'boxofficemojo')
METACRITIC_DIR = os.path.join(DATA_DIR, 'metacritic')


def get_metacritic_movies():
    """Returns a list of dictionaries for each Metacritic movie entry
    available. Ready to be loaded into a Pandas dataframe."""

    movies = []
    for metadict in _iter_json_dicts(METACRITIC_DIR):
        if isinstance(metadict, dict):
            if 'unable to retrieve' not in metadict.keys():
                movie_object = MetacriticMovie(metadict)
                movies.append(movie_object.__dict__)

    return movies


def get_mojo_movies():
    """Returns a list of dictionaries for each BoxOfficeMojo movie entry
    available. Ready to be loaded into a Pandas dataframe."""

    movies = []
    for mojodict in _iter_json_dicts(MOJO_DIR):
        if isinstance(mojodict, dict):
            movie_object = MojoMovie(mojodict)
            movies.append(movie_object.__dict__)

    return movies


# internal functions & classes
def _iter_json_dicts(dir_path):
    """Iterator that yields dictionaries from JSON files in the specified dir"""
    filenames = os.listdir(dir_path)
    for filename in filenames:
        if not filename.startswith("_"):
            filepath = os.path.join(dir_path, filename)
            with open(filepath, 'rb') as infile:
                yield json.load(infile)
