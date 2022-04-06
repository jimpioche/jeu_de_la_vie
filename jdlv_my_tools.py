# -*- coding: utf-8 -*-
"""

"""

from os import listdir
from os.path import isfile, join
import random
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 

from jdlv_data import * 
from jdlv_model import *
from jdlv_outils import *

def clean_grid (grid):
    for i in range (default_grid_size):
        for j in range (default_grid_size):
            grid.cases [i][j]['s'] = death_status
            grid.cases [i][j]['c'] = death_color
    return grid

def make_conway (grid, i, j, color):
    #grid = clean_grid (grid)
    cases = grid.cases
    cases [i] [j] ['s'] = life_status
    cases [i] [j] ['c'] = color
    cases [i] [j + 1] ['s'] = life_status
    cases [i] [j + 1] ['c'] = color
    cases [i - 1] [j + 1] ['s'] = life_status
    cases [i - 1] [j + 1] ['c'] = color
    cases [i - 1] [j + 2] ['s'] = life_status
    cases [i - 1] [j + 2] ['c'] = color
    cases [i - 2] [j + 1] ['s'] = life_status
    cases [i - 2] [j + 1] ['c'] = color
    return grid
    
def apply_game_of_life_rules (grid):
    previous_grid = grid
    previous_cases = previous_grid.cases
    cases = grid.cases # cases is a list of lists of dictionnaries
    next_grid = Grid (len (cases))
    next_cases = next_grid.cases
    for i in range (1, len (cases) - 1):
        for j in range (1, len (cases) - 1):
            previous_status = cases [i][j]['s']
            voisins = get_voisins (cases, i, j)
            nbre_alive_voisins = count_alive_voisins (voisins)
            if nbre_alive_voisins == 3:
                next_cases [i] [j] = revive_case (next_cases [i] [j])
            elif nbre_alive_voisins <= 1 or nbre_alive_voisins >= 4:
                next_cases [i] [j] = kill_case (next_cases [i] [j])
            else:
                next_cases [i] [j] = cases [i] [j]
    return next_grid

def apply_rules (grid):
    for i in range (10):
        next_grid = apply_game_of_life_rules (grid)
    return next_grid
