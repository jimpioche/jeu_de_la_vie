import sys
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTextBrowser
from PyQt5.QtGui import QIcon, QPixmap


def qmessage_box (title, message):
    msgBox = QMessageBox()
    msgBox.setStyleSheet("QLabel{min-width: 800px;}")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
    msgBox.setWindowIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setInformativeText(message)
    msgBox.exec_()

def qmessage_box_with_cancel (title, message):
    msgBox = QMessageBox ()
    msgBox.setStyleSheet ("QLabel{min-width: 500px;}");
    msgBox.setWindowTitle (title)
    msgBox.setInformativeText (message)
    msgBox.setStandardButtons (QMessageBox.Cancel | QMessageBox.Yes)
    answer = msgBox.exec_ ()
    return answer

def information_with_cancel (message):
    title = "Information"
    answer = qmessage_box_with_cancel (title, message)
    return answer
