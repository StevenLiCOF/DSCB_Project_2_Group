"""loaddata is a module for accessing scraped data about movies from
BoxOfficeMojo and Metacritic.
It's built specifically to work with the data collected for the
CapitalOne Metis Data Science Python Bootcamp Pilot Extravaganza 2K15.
"""

# imports
import os

# constants
DATA_DIR = os.path.abspath('data')
MOJO_DIR = os.path.join(DATA_DIR, 'boxofficemojo')


