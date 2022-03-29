# -*- coding:utf-8 -*-
"""

"""

import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, \
    QThread, QThreadPool, pyqtSignal

#from jdlv_vue_fromUi import *
#from jdlv_model import *
from jdlv_vue import *
from jdlv_controleur import *
from jdlv_outils import *
from jdlv_data import *
#from pyqt5_utils import *


class App:
    def __init__(self, args):
        #QtWidgets.QApplication.setAttribute (QtCore.Qt.AA_EnableHighDpiScaling)
        self.qtapp = QtWidgets.QApplication (args)
        self.grid = Grid (default_grid_size)
        self.vue = Vue (self.grid)
        self.controleur = Ctrl_vue (self.vue)
        self.vue.show ()
        self.vue.update (self.grid)
        self.vue.setWindowTitle (game_name + "      "  + default_empty_file_name)
        self.qtapp.exec_ ()

def main (args):
    #cpmi_dir = os.makedirs (os.path.expanduser(r'~')+u"/cpmi_v__")
    #sys.stdout = open (cpmi_dir + '/sismicCPMI__stdout', 'w')
    #sys.stderr = open (cpmi_dir + '/sismicCPMI__stderr', 'w')
    
    mapp = App (args)
    #sys.exit(mapp.exec_())

# __name__ : variable créée automatiquement par python
# Pour éviter l'exécution du script lors de l'import.
# Dans notre cas la variable __name__ contient la chaine de caractère "__main__".

if __name__ == "__main__":
    main (sys.argv)
