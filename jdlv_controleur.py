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
from jdlv_my_tools import *
from jdlv_other_functions import *
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
        self.fisrt_case_for_copying = None
        self.second_case_for_copying = None
        self.fisrt_case_for_erasing = None
        self.second_case_for_erasing = None
        self.copied_cases = None
        self.playing_or_pausing = "pausing"
        self.is_paused = True
        self.is_playing = False
        self.is_killed = False
        self.is_copying = False
        self.is_pasting = False
        self.is_erasing = False
        self.current_grid_may_not_be_the_shown_grid = False
        #self.theading_event = threading.Event ()
        self.comm = Communicate ()
        self.comm.update_vue.connect (self.action_signal_update_vue_emited)
        self.vue.ui.pb_play_pause.clicked.connect ( \
            self.action_pb_play_pause_clicked)
        self.vue.ui.pb_redo_play.clicked.connect (self.action_pb_redo_play_clicked)
        self.vue.ui.pb_undo_play.clicked.connect (self.action_pb_undo_play_clicked)
        self.vue.ui.pb_reset.clicked.connect (self.action_pb_reset_clicked)
        self.vue.ui.pb_save.clicked.connect (self.action_pb_save_clicked)
        self.vue.ui.pb_save_as.clicked.connect (self.action_pb_save_as_clicked)
        self.vue.ui.pb_load.clicked.connect (self.action_pb_load_clicked)
        self.vue.ui.pb_quit.clicked.connect (self.action_pb_quit_clicked)
        # self.vue.ui.pb_copier_coller.clicked.connect ( \
        #     self.action_pb_copier_coller_clicked)
        self.vue.ui.pb_copier.clicked.connect ( \
            self.action_pb_copier_clicked)
        self.vue.ui.pb_coller.clicked.connect ( \
            self.action_pb_coller_clicked)
        self.vue.ui.pb_effacer.clicked.connect ( \
            self.action_pb_effacer_clicked)
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

    def disconnect_widget (self, widget):
        widget.disconnect ()

    def connect_widget_signal_action (self, widget, signal, action):
        command = \
            str (widget) + "." + str (signal) + ".connect (" + str (action) + ")"
        eval (command)

    def action_pb_play_from_scene_clicked (self):
        pass

    def action_pb_copier_clicked (self):
        #print ("\nCopying...")
        self.is_copying = True
        self.is_pasting = False

    def action_pb_coller_clicked (self):
        #print ("\nPasting...")
        self.is_pasting = True
        self.is_copying = False

    def action_pb_effacer_clicked (self):
        #print ("\nErasing...")
        self.is_erasing = True

    def action_tablew_grid_cellClicked_while_copying (self, i, j):
        #print ("\nClicking in tablew_grid...")
        if self.fisrt_case_for_copying == None:
            self.fisrt_case_for_copying = self.vue.grid.cases [i] [j]
            self.first_i_for_copying = i
            self.first_j_for_copying = j
            #print ("(self.first_i_for_copying, self.first_j_for_copying) = " \
            #       + str ((self.first_i_for_copying, self.first_j_for_copying)))
        else:
            if self.second_case_for_copying == None:
                self.second_case_for_copying = self.vue.grid.cases [i] [j]
                self.second_i_for_copying = i
                self.second_j_for_copying = j
                #print ("(self.second_i_for_copying, self.second_j_for_copying) = " \
                #       + str ((self.second_i_for_copying, self.second_j_for_copying)))
        if self.fisrt_case_for_copying != None \
           and self.second_case_for_copying != None \
               and self.is_pasting:
            self.first_i_for_pasting = i
            self.first_j_for_pasting = j
            i_gap = abs (self.second_i_for_copying - self.first_i_for_copying)
            j_gap = abs (self.second_j_for_copying - self.first_j_for_copying)
            #print ("(i_gap, j_gap) = " + str ((i_gap, j_gap)))
            #print ("(self.first_i_for_pasting, self.first_j_for_pasting) = " \
            #         + str ((self.first_i_for_pasting, self.first_j_for_pasting)))
            for m in range (i_gap):
                for n in range  (j_gap):
                    self.vue.grid.cases \
                        [self.first_i_for_pasting + m] \
                        [self.first_j_for_pasting + n] ["s"] = \
                            self.vue.grid.cases [self.first_i_for_copying + m] \
                                                        [self.first_j_for_copying + n] ["s"]
                    self.vue.grid.cases \
                        [self.first_i_for_pasting + m] \
                        [self.first_j_for_pasting + n] ["c"] = \
                            self.vue.grid.cases [self.first_i_for_copying + m] \
                                                        [self.first_j_for_copying + n] ["c"]
            self.fisrt_case_for_copying = None
            self.second_case_for_copying = None
            self.is_pasting = None
            self.is_copying = None
        self.vue.update (self.vue.grid)

    def action_pb_copier_coller_clicked (self):
        if self.vue.ui.pb_copier_coller.text () == text_copier:
            #print ("\nCopying  clicked...\n")
            #self.vue.ui.tablew_grid.disconnect ()
            self.vue.ui.tablew_grid.cellClicked.connect ( \
                self.action_tablew_grid_cellClicked_while_copying)
            set_text_line_edit (self.vue.ui.pb_copier_coller, text_coller)
            self.copying_available = False
            self.is_copying = True
            self.is_pasting = False
            self.pasting_available = True
        else:
            #print ("\nPasting  clicked...\n")
            set_text_line_edit (self.vue.ui.pb_copier_coller, text_copier)
            self.copying_available = True
            self.is_copying = False
            self.is_pasting = True
            self.pasting_available = False
            #self.vue.ui.tablew_grid.disconnect ()
            #self.vue.ui.tablew_grid.itemSelectionChanged.connect ( \
            #    self.action_tablew_grid_itemSelectionChanged)

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
            self.current_undo_grid = self.saved_grids_for_undo.pop ()
            self.saved_grids_for_redo.append (self.current_undo_grid)
            #self.current_grid_may_not_be_the_shown_grid = True
            self.vue.grid = self.current_undo_grid
            self.vue.update (self.vue.grid)
        except:
            pass

    def action_pb_redo_play_clicked (self):
        try:
            self.current_redo_grid = self.saved_grids_for_redo.pop ()
            self.saved_grids_for_undo.append (self.current_redo_grid)
            self.vue.grid = self.current_redo_grid
            self.vue.update (self.vue.grid)
        except:
            pass

    def grid_shown_in (self, table_widget):
        for i in range (table_widget.rowCount ()):
            for j in range (table_widget.columnCount ()):
                item = table_widget.item (i, j)
                color = item.background ().color ()
                print ("color = " + str (color))
        return "Ok"

    def bidon (self):
        pass

    def action_pb_play_pause_clicked (self):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vue.set_icon ( \
                                self.vue.ui.pb_play_pause, ":/newPrefix/play.PNG")
            self.vue.ui.pb_play_pause.setText ("Play")
        else:
            self.is_playing = True
            self.is_paused = False
            self.vue.set_icon ( \
                                self.vue.ui.pb_play_pause, ":/newPrefix/pause.PNG")
            self.vue.ui.pb_play_pause.setText ("Pause")
            self.saved_grids_for_undo.append (self.vue.grid)
        starting_grid = self.vue.grid
        compteur = 0
        while True:
            if self.is_paused:
                break
            else:
                QApplication.processEvents ()
                self.next_grid = apply_rules (starting_grid, compteur)
                self.vue.update (self.next_grid)
                starting_grid = self.next_grid
                compteur += 1
        self.vue.grid = self.next_grid

    def action_pb_reset_clicked (self):
        self.saved_grids_for_undo = []
        self.saved_grids_for_redo = []
        self.vue.grid = clean_grid (self.vue.grid)
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
        #print ("\nitem Selection Changed ....signal")
        selected_indexes = self.vue.ui.tablew_grid.selectedIndexes ()
        if not (self.is_copying) and not (self.is_pasting):
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
        if self.is_copying and not (self.is_pasting) and not (self.is_erasing):
            i = selected_indexes [0].row ()
            j = selected_indexes [0].column ()
            if self.fisrt_case_for_copying == None:
                self.fisrt_case_for_copying = self.vue.grid.cases [i] [j]
                self.first_i_for_copying = i
                self.first_j_for_copying = j
                #print ("(self.first_i_for_copying, self.first_j_for_copying) = " \
                #       + str ((self.first_i_for_copying, self.first_j_for_copying)))
            else:
                if self.second_case_for_copying == None:
                    self.second_case_for_copying = self.vue.grid.cases [i] [j]
                    self.second_i_for_copying = i
                    self.second_j_for_copying = j
                    #print ("(self.second_i_for_copying, self.second_j_for_copying) = " \
                    #       + str ((self.second_i_for_copying, self.second_j_for_copying)))
                    self.is_copying = False
        if not (self.is_copying) and self.is_pasting and not (self.is_erasing):
            i = selected_indexes [0].row ()
            j = selected_indexes [0].column ()
            if self.fisrt_case_for_copying != None \
               and self.second_case_for_copying != None:
                self.first_i_for_pasting = i
                self.first_j_for_pasting = j
                i_gap = abs (self.second_i_for_copying - self.first_i_for_copying)
                j_gap = abs (self.second_j_for_copying - self.first_j_for_copying)
                #print ("(i_gap, j_gap) = " + str ((i_gap, j_gap)))
                #print ("(self.first_i_for_pasting, self.first_j_for_pasting) = " \
                #         + str ((self.first_i_for_pasting, self.first_j_for_pasting)))
                for m in range (i_gap):
                    for n in range  (j_gap):
                        self.vue.grid.cases \
                            [self.first_i_for_pasting + m] \
                            [self.first_j_for_pasting + n] ["s"] = \
                                self.vue.grid.cases [self.first_i_for_copying + m] \
                                                            [self.first_j_for_copying + n] ["s"]
                        self.vue.grid.cases \
                            [self.first_i_for_pasting + m] \
                            [self.first_j_for_pasting + n] ["c"] = \
                                self.vue.grid.cases [self.first_i_for_copying + m] \
                                                            [self.first_j_for_copying + n] ["c"]
                self.fisrt_case_for_copying = None
                self.second_case_for_copying = None
                self.is_pasting = False
        if not (self.is_copying) and not (self.is_pasting) and self.is_erasing:
            i = selected_indexes [0].row ()
            j = selected_indexes [0].column ()
            if self.fisrt_case_for_erasing == None:
                self.fisrt_case_for_erasing = self.vue.grid.cases [i] [j]
                self.first_i_for_erasing = i
                self.first_j_for_erasing = j
                #print ("(self.first_i_for_erasing, self.first_j_for_erasing) = " \
                #       + str ((self.first_i_for_erasing, self.first_j_for_erasing)))
            else:
                if self.second_case_for_erasing == None:
                    self.second_case_for_erasing = self.vue.grid.cases [i] [j]
                    self.second_i_for_erasing = i
                    self.second_j_for_erasing = j
                    #print ("(self.second_i_for_erasing, self.second_j_for_erasing) = " \
                    #       + str ((self.second_i_for_erasing, self.second_j_for_erasing)))
                    for m in range (self.first_i_for_erasing, self.second_i_for_erasing):
                        for n in range (self.first_j_for_erasing, self.second_j_for_erasing):
                            self.vue.grid.cases [m] [n] ['s'] = 0
                            self.vue.grid.cases [m] [n] ['c'] = death_color
                    self.fisrt_case_for_erasing = None
                    self.second_case_for_erasing = None
                    self.is_erasing = False
        self.vue.update (self.vue.grid)

        
    
