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


def adapter_affichage_du_tablewidget ( \
                                       tablew, \
                                       horizontal_entetes, \
                                       vertical_entetes, \
                                       grid_size):
    tablew.setColumnCount (grid_size)
    tablew.setRowCount (grid_size)
    tablew.horizontalHeader().hide()
    tablew.verticalHeader().hide()
    for i in range (grid_size):
        tablew.setColumnWidth (i, cell_width)
        tablew.setRowHeight (i, cell_height)

def set_tablew_item_color (tablew, i, j, brush):
    tablew.blockSignals (True)
    item = tablew.item (int(i), int(j))
    item.setBackground (brush)
    tablew.blockSignals (False)

def set_tablew_item_text (tablew, i, j, color):
    tablew.blockSignals (True)
    tablew.item (int(i), int(j)).setText (value)
    tablew.blockSignals (False)

def ajouter_items_dans_la_ligne (tablew, num_ligne):
    for j in range (tablew.columnCount ()):
        item = QtWidgets.QTableWidgetItem ()
        tablew.blockSignals (True)
        tablew.setItem (num_ligne, j, item)
        tablew.blockSignals (False)
    
def ajouter_a_la_fin_une_ligne_avec_ses_items (tablew):
    """ ajoute une ligne à la fin du tablewidget de nom tablew """
    nbre_ligne = tablew.rowCount ()
    tablew.insertRow (nbre_ligne)
    ajouter_items_dans_la_ligne (tablew, nbre_ligne)

def add_items_in_combo (list_of_items, combo):
    if list_of_items != None:
        combo.blockSignals (True)
        combo.clear ()
        combo.addItems (list_of_items)
        combo.setCurrentIndex (-1)
        combo.blockSignals (False)
    
def qmessage_box (title, message):
    msgBox = QMessageBox ()
    msgBox.setStyleSheet("QLabel{min-width: 800px;}")
    # icon = QtGui.QIcon()
    # icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
    # msgBox.setWindowIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setInformativeText(message)
    msgBox.exec_()

def print_message (title, message):
    qmessage_box (title, message)

def information (message):
    title = "Information"
    print_message (title, message)

def is_alive (case):
    return case ['s'] == life_status

def is_dead (case):
    return not (is_alive (case))

def get_voisins (cases, i, j):
    voisins = \
                [cases[i-1][j+1], cases[i][j+1], cases[i+1][j+1], cases[i-1][j], \
                 cases[i+1][j], cases[i-1][j-1], cases[i][j-1], cases[i+1][j-1]]
    return voisins

def count_alive_voisins (voisins):
    cpt = 0
    for voisin in voisins:
        if is_alive (voisin):
            cpt = cpt + 1
    return cpt

def kill_case (case):
    case ["s"] = death_status
    case ["c"] = death_color
    return case

def revive_case (case):
    case ["s"] = life_status
    case ["c"] = life_color
    return case

def apply_life_rules (grid):
    previous_grid = grid
    previous_cases = previous_grid.cases
    cases = grid.cases # cases is a list of lists of dictionnaries
    next_grid = Grid (len (cases))
    next_cases = next_grid.cases
    some_case_changed_its_status = False
    for i in range (1, len (cases) - 1):
        for j in range (1, len (cases) - 1):
            previous_status = cases [i][j]['s']
            voisins = get_voisins (cases, i, j)
            nbre_alive_voisins = count_alive_voisins (voisins)
            if nbre_alive_voisins == 3:
                next_cases [i] [j] = revive_case (next_cases [i] [j])
                if previous_status != life_status:
                    some_case_changed_its_status = True
            elif nbre_alive_voisins <= 1 or nbre_alive_voisins >= 4:
                next_cases [i] [j] = kill_case (next_cases [i] [j])
                if previous_status != death_status:
                    some_case_changed_its_status = True
            else:
                next_cases [i] [j] = cases [i] [j]
    return next_grid
    
    # # #####   Loup - RENARD - BELETTE   
    # cases = grid.cases # cases is a list of lists of dictionnaries
    # some_case_changed_its_status = False
    # for i in range (1, len (cases) - 1):
    #     for j in range (1, len (cases) - 1):
    #         previous_status = cases [i][j]['s']
    #         voisins = get_voisins (cases, i, j)
    #         nbre_alive_voisins = count_alive_voisins (voisins)
    #         if nbre_alive_voisins == 3 or nbre_alive_voisins == 2:
    #             cases [i][j] = revive_case (cases [i][j])
    #             if previous_status != life_status:
    #                 some_case_changed_its_status = True
    #         elif nbre_alive_voisins <= 1 or nbre_alive_voisins >= 4:
    #             cases[i][j] = kill_case (cases[i][j])
    #             if previous_status != death_status:
    #                 some_case_changed_its_status = True
    #         else:
    #             pass
    # return grid

def json_load (fname):
        file = open (fname, "r")
        data_from_json = json.load (file)
        file.close ()
        return data_from_json

def json_dump (cases, fname):
    out_file = open (fname, "w")
    json.dump (cases, out_file, indent = 6)
    out_file.close ()

def read_files_in (dir):
    fichiers = [f for f in listdir (dir) if isfile (join (dir + "/", f))]
    return fichiers

def make_combo_items (files):
    files_items = []
    for i in range (len (files)):
        files_items.append (str (files [i]))
    return files_items

def set_text_widget (widget, e):
    widget.blockSignals (True)
    if e == None:
        widget.setText (None)
    else:
        widget.setText (str (e))        
    widget.blockSignals (False)

set_text_line_edit = set_text_widget
set_text_label = set_text_widget
set_text_push_button = set_text_widget
