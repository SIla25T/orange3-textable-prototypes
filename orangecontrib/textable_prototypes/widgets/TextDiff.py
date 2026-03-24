"""Code du widget TextDiff"""
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from Orange.data import Table
from AnyQt.QtWidgets import (
    QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy
)
from AnyQt.QtCore import Qt
from AnyQt.QtGui import QFont


class TextDiff(OWWidget):
    name = "Text Diff"
    description = "Compare deux listes de segments et affiche les différences."
    icon = "icons/Text_Diff.png" 
    priority = 10

    want_main_area = False
    resizing_enabled = True