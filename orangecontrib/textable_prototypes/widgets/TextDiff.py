"""Code du widget TextDiff"""
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import widget, gui
from Orange.data import Table
from AnyQt.QtWidgets import (
    QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy
)
from AnyQt.QtCore import Qt
from AnyQt.QtGui import QFont
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview


class TextDiff(OWWidget):
    """An Orange widget that compares two versions of a translated text and displays the differences."""

    #----------------------------------------------------------------------
    # Widget's metadata...

    name = "Text Diff"
    description = "Compare deux listes de segments et affiche les différences."
    icon = "icons/Text_Diff.png" 
    priority = 10

    #----------------------------------------------------------------------
    # Channel definitions...
    class Inputs:
        A = Input("A", int)
        B = Input("B", int)
    
    class Outputs:
        comparison_result = Output("Comparison result", int)

    #----------------------------------------------------------------------
    # GUI layout parameters...

    want_main_area = False
    resizing_enabled = True

    #----------------------------------------------------------------------
    # Settings declaration and initializations (default values)...
    
    selected_segmentation_type = Setting("words")

    def __init__(self):
        super().__init__()

        self.a = None
        self.b = None
        
        #----------------------------------------------------------------------
        # User interface...

        gui.comboBox(
            widget=self.controlArea,
            master=self,
            value='selected_segmentation_type',
            label='Select a segmentation type: ',
            tooltip='words : words\nsentences : sentences',
            items=['words', 'sentences'],
            sendSelectedValue=True,
            callback=self.handleNewSignals,
        )
        self.label = gui.widgetLabel(self.controlArea, "2 inputs are needed.")

    @Inputs.A
    def set_A(self, a):
        """Set the input 'A'."""
        self.a = a
        self.handleNewSignals()

    @Inputs.B
    def set_B(self, b):
        """Set the input 'B'."""
        self.b = b
        self.handleNewSignals()

    def handleNewSignals(self):
        """Reimplemented from OWWidget."""
        if self.a is not None and self.b is not None:
            if self.selected_segmentation_type == "words":
                # à remplacer par des regex qui sépare par mots
                result = self.a + self.b
            elif self.selected_segmentation_type == "sentences":
                # à remplacer par des regex qui sépare par phrases
                result = self.a - self.b
            # jsp ce que ça fait mais à modifier/enlever :
            self.label.setText(
                "%i %s %i = %i" % (
                    self.a,
                    self.selected_segmentation_type,
                    self.b, 
                    result,
                )
            )
            self.Outputs.operation_result.send(result)
        else:
            self.label.setText("2 inputs are needed.")
            # Clear the channel by sending None.
            self.Outputs.operation_result.send(None)
