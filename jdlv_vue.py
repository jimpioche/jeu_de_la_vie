# -*- coding:utf-8 -*-
"""

"""
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *

from jdlv_vue_fromUi import *
#from jdlv_model import *
from jdlv_outils import *
from jdlv_data import *
from jdlv_qrc import *

class Vue (QtWidgets.QWidget):
    def __init__(self, grid=None):
        QtWidgets.QWidget.__init__ (self)
        self.ui = Ui_Form ()
        self.ui.setupUi (self)
        self.grid = grid
        self.current_grid_size = len (grid.cases)
        self.default_input_dir_name = default_input_dir_name
        adapter_affichage_du_tablewidget (self.ui.tablew_grid, \
                                                              horizontal_tablew_headers, \
                                                              vertical_tablew_headers, \
                                                              self.current_grid_size)
        self.fill_tablew_with_items ()
        #self.ui.tablew_grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.add_examples_in_cb_figures_de_bases ()
        self.ui.pb_play_pause.setText ("Play")
        self.set_icon (self.ui.pb_play_pause, ":/newPrefix/play.PNG")
        self.set_icon (self.ui.pb_reset, ":/newPrefix/mur_rouge.png")
        self.set_icon (self.ui.pb_save, ":/newPrefix/sauver.png")
        self.set_icon (self.ui.pb_save_as, ":/newPrefix/enregistrer_sous.png")
        self.set_icon (self.ui.pb_load, ":/newPrefix/url.png")
        self.set_icon (self.ui.pb_quit, ":/newPrefix/quitter.png")
        self.set_icon (self.ui.pb_effacer, ":/newPrefix/erase.png")
        self.set_icon (self.ui.pb_copier, ":/newPrefix/copier.png")
        self.set_icon (self.ui.pb_coller, ":/newPrefix/coller.png")

    def add_examples_in_cb_figures_de_bases (self):
        try:
            figures_de_base_names = read_files_in (default_input_dir_name)
            figures_de_base_items = make_combo_items (figures_de_base_names)
            add_items_in_combo (figures_de_base_items, self.ui.cb_figures_de_base)
        except:
            pass
        #print ("No examples for loading ! ")

    def set_icon (self, push_button, png_file):
        icon = QtGui.QIcon()
        icon.addPixmap (QtGui.QPixmap (png_file), \
                                  QtGui.QIcon.Normal, QtGui.QIcon.On)
        push_button.setIcon (icon)
        push_button.setIconSize (QtCore.QSize (32, 32))

    def fill_tablew_with_items (self):
        for i in range (self.current_grid_size):
            for j in range (self.current_grid_size):
                item = QtWidgets.QTableWidgetItem ()
                self.ui.tablew_grid.setItem (i, j, item)

    def update (self, grid):
        for i in range (len (grid.cases)):
            for j in range (len (grid.cases)):
                color = grid.cases [i] [j] ['c']
                brush = brushes [color]
                # if color == life_color:
                #     brush = brushes [color]
                # else:
                #     brush = death_brush
                set_tablew_item_color (self.ui.tablew_grid, i, j, brush)
