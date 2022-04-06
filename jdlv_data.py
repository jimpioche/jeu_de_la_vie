import os, sys
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *

default_grid_size = 100
N = default_grid_size

game_name = "Jeu de la vie :"
#tablew_headers = [str (i)  for i in range (N)]
horizontal_tablew_headers = [""  for i in range (N)]
vertical_tablew_headers = ["\n\n"  for i in range (N)]

historique = []

rotation_period = 4

cell_width = 10
cell_height = cell_width

life_status = 1
life_color = 'black'
life_brush = QtGui.QBrush (QtGui.QColor (life_color))
death_status = 0
death_color = 'white'
death_brush = QtGui.QBrush (QtGui.QColor (death_color))

colors = ["red", "blue", "yellow", "pink", "green", "black", "white"]
brushes = {}
for color in colors:
    brushes [color] = QtGui.QBrush (QtGui.QColor (color))

default_empty_file_name = "Untitled.jdlv"

text_enregistrer_sous = "Enregistrer sous"
text_directory_of_examples ="Répertoire d'exemples .jdlv"
message_change_starting_grid = \
    "Souhaitez-vous repartir de la configuration qui apparait " \
    "actuellement sur la grille ?"

if not os.path.exists (os.path.expanduser (r'~') + "/jeu_de_la_vie"):
    os.makedirs (os.path.expanduser (r'~') + "/jeu_de_la_vie")
default_input_dir_name = os.path.expanduser (r'~') + "jeu_de_la_vie"
    
figures_de_bases = ['le clignotant', 'le glisseur', 'le crapaud', 'le canon à glisseur']
dico_figures_de_base = \
    { \
      'le clignotant' : default_input_dir_name + "/le_clignotant.jdlv", \
      'le glisseur' : default_input_dir_name + "/le_glisseur.jdlv", \
      'le crapaud' : default_input_dir_name + "/le_crapaud.jdlv", \
      'le canon à glisseur' : default_input_dir_name + "/le_canon_a_glisseurs.jdlv" \
    }      

text_loading_failed = "Le fichier n'a pas pu être téléchargé..."
text_copier = "Copier"
text_coller = "Coller"
