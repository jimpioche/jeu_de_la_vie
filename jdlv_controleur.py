# -*- coding: utf-8 -*-
"""

"""
import os
import sys
import time
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


from jdlv_vue import *
from jdlv_vue_fromUi import *
#from jdlv_model import *
from jdlv_outils import *
from jdlv_data import *
from jdlv_qrc import *
#from pyqt5_utils import *


class Communicate (QObject):
    update_vue = pyqtSignal ()


class Ctrl_vue ():
    def __init__(self, vue=None):
        self.vue = vue
        self.grid = self.vue.grid
        self.saved_grids_for_undo = []
        self.saved_grids_for_redo = []
        self.playing_or_pausing = "pausing"
        self.is_paused = True
        self.is_playing = False
        self.is_killed = False
        #self.theading_event = threading.Event ()
        self.comm = Communicate ()
        self.comm.update_vue.connect (self.action_signal_update_vue_emited)
        self.vue.ui.pb_play_pause.clicked.connect (self.action_pb_play_pause_clicked)
        self.vue.ui.pb_redo_play.clicked.connect (self.action_pb_redo_play_clicked)
        self.vue.ui.pb_undo_play.clicked.connect (self.action_pb_undo_play_clicked)
        self.vue.ui.pb_reset.clicked.connect (self.action_pb_reset_clicked)
        self.vue.ui.pb_save.clicked.connect (self.action_pb_save_clicked)
        self.vue.ui.pb_save_as.clicked.connect (self.action_pb_save_as_clicked)
        self.vue.ui.pb_load.clicked.connect (self.action_pb_load_clicked)
        self.vue.ui.pb_quit.clicked.connect (self.action_pb_quit_clicked)
        self.vue.ui.pb_add_examples.clicked.connect ( \
            self.action_pb_add_examples_clicked)
        self.vue.ui.tablew_grid.itemSelectionChanged.connect ( \
            self.action_tablew_grid_itemSelectionChanged)
        #self.vue.ui.tablew_grid.selectionModel ().currentChanged.connect ( \
        #    self.action_tablew_grid_cellClicked)
        #self.vue.ui.tablew_grid.selectionModel ().selectionChanged.connect ( \
        #    self.action_tablew_selectionChanged)
        self.vue.ui.cb_figures_de_base.currentIndexChanged.connect ( \
                        self.action_cb_figures_de_base__currentIndexChanged)
        self.next_grid = None
        self.fname = None

    def action_pb_add_examples_clicked (self):
        dialog_res = \
            QtWidgets.QFileDialog.getExistingDirectory ( \
                self.vue, \
                text_directory_of_examples, \
                self.vue.default_input_dir_name)
        self.vue.default_input_dir_name = dialog_res
        #print (str (self.vue.default_input_dir_name))
        if self.vue.default_input_dir_name not in ["", None]:
            figures_de_base_names = read_files_in (self.vue.default_input_dir_name)
            figures_de_base_items = make_combo_items (figures_de_base_names)
            add_items_in_combo ( \
                                 figures_de_base_items, self.vue.ui.cb_figures_de_base)
        else:
            pass
        
    def action_signal_update_vue_emited (self):
        #print ("updating the view !!!!!!")
        self.vue.update (self.next_grid)

    def action_pb_undo_play_clicked (self):
        try:
            grid = self.saved_grids_for_undo.pop ()
            self.saved_grids_for_redo.append (grid)
            self.vue.update (grid)
        except:
            pass

    def action_pb_redo_play_clicked (self):
        try:
            grid = self.saved_grids_for_redo.pop ()
            self.saved_grids_for_undo.append (grid)
            self.vue.update (grid)
        except:
            pass

    def action_pb_play_pause_clicked (self):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vue.set_icon (self.vue.ui.pb_play_pause, ":/newPrefix/play.PNG")
            self.vue.ui.pb_play_pause.setText ("Play")
        else:
            self.is_playing = True
            self.is_paused = False
            self.vue.set_icon (self.vue.ui.pb_play_pause, ":/newPrefix/pause.PNG")
            self.vue.ui.pb_play_pause.setText ("Pause")
            self.saved_grids_for_undo.append (self.vue.grid)
        some_status_changed = True
        starting_grid = self.vue.grid
        while True:
            if self.is_paused:
                break
            else:
                #print ("Calculating next_grid")
                QApplication.processEvents ()
                self.next_grid = apply_life_rules (starting_grid)
                self.vue.update (self.next_grid)
                #self.comm.update_vue.emit ()
                starting_grid = self.next_grid
        self.vue.grid = self.next_grid

    def action_pb_reset_clicked (self):
        self.saved_grids_for_undo = []
        self.saved_grids_for_redo = []
        for i in range (self.vue.current_grid_size):
            for j in range (self.vue.current_grid_size):
                self.vue.grid.cases [i][j]['s'] = death_status
                self.vue.grid.cases [i][j]['c'] = death_color
        self.vue.update (self.vue.grid)

    def action_pb_save_as_clicked (self):
        dialog_res = \
          QtWidgets.QFileDialog.getSaveFileName (\
                    self.vue, text_enregistrer_sous, default_input_dir_name, "*.jdlv")
        self.fname = dialog_res [0]
        if self.fname in ["", None, default_empty_file_name]:
            pass
        else:
            json_dump (self.vue.grid.cases, self.fname)
            self.vue.setWindowTitle (game_name + "      "  + str (self.fname))

    def action_pb_save_clicked (self):
        # the json file where the output must be stored
        if self.fname in ["", None, default_empty_file_name]:
            self.action_pb_save_as_clicked ()
        else:
            json_dump (self.vue.grid.cases, self.fname)
        self.vue.setWindowTitle (game_name + "      "  + str (self.fname))

    def load_file (self, file):
        try:
            json_cases = json_load (file)
            self.vue.grid.fill_grid_with_cases (json_cases)
            #self.vue.grid.cases = json_cases
            self.vue.current_grid_size = len (self.vue.grid.cases)
            current_tablew_size = self.vue.ui.tablew_grid.columnCount ()
            #print ("self.vue.current_grid_size = " + str (self.vue.current_grid_size))
            #print ("current_tablew_size = " + str (current_tablew_size))       
            if self.vue.current_grid_size > current_tablew_size:
                adapter_affichage_du_tablewidget (self.vue.ui.tablew_grid, \
                                                              horizontal_tablew_headers, \
                                                              vertical_tablew_headers, \
                                                              self.vue.current_grid_size)
                self.vue.fill_tablew_with_items ()
            self.vue.update (self.vue.grid)
            self.vue.setWindowTitle (game_name + "      "  + str (file))
        except:
            information (str (file) + '\n\n' + text_loading_failed)

    def action_pb_load_clicked (self):
      dialog_res = \
        QtWidgets.QFileDialog.getOpenFileName ( \
                                                self.vue, \
                                                "Ouvrir un fichier", \
                                                default_input_dir_name, "*.jdlv")
      self.fname = dialog_res [0]
      self.load_file (self.fname)

    def action_pb_quit_clicked (self):
        sys.exit (0)

    def action_cb_figures_de_base__currentIndexChanged (self):
        currentText = self.vue.ui.cb_figures_de_base.currentText ()
        self.fname = self.vue.default_input_dir_name + "/" + currentText
        self.load_file (self.fname)

    def a_case_is_alive_in_the_selection (self, selected_indexes):
        reponse = False
        for ix in selected_indexes:
            i = ix.row ()
            j = ix.column ()
            case = self.vue.grid.cases [i] [j]
            if is_alive (case):
                reponse = True
                break
        return reponse

    def action_tablew_grid_itemSelectionChanged (self):
        selected_indexes = self.vue.ui.tablew_grid.selectedIndexes ()
        if len (selected_indexes) == 1:
            i = selected_indexes [0].row ()
            j = selected_indexes [0].column ()
            case = self.vue.grid.cases [i] [j]
            if is_alive (case):
                case = kill_case (case)
            else:
                case = revive_case (case)
        else:
            for ix in selected_indexes:
                i = ix.row ()
                j = ix.column ()
                case = self.vue.grid.cases [i] [j]
                case = revive_case (case)
            # if self.a_case_is_alive_in_the_selection (selected_indexes):
            #     for ix in selected_indexes:
            #         i = ix.row ()
            #         j = ix.column ()
            #         case = self.vue.grid.cases [i] [j]
            #         case = kill_case (case)
            # else:
            #     for ix in selected_indexes:
            #         i = ix.row ()
            #         j = ix.column ()
            #         case = self.vue.grid.cases [i] [j]
            #         case = revive_case (case)
        self.vue.update (self.vue.grid)

        
    
