# Standard imports...
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from Orange.widgets.utils.widgetpreview import WidgetPreview

__version__ = "0.01"


class DisplayInt(widget.OWWidget):
    """An Orange widget that lets the user display an integer value"""

    #----------------------------------------------------------------------
    # Widget's metadata...

    name = "Display Integer"
    description = "Display an integer value"
    icon = "icons/mywidget.svg"
    priority = 30

    #----------------------------------------------------------------------
    # Channel definitions (NB: no output in this case)...

    class Inputs:
        integer = Input("Integer", int)

    #----------------------------------------------------------------------
    # GUI layout parameters...

    want_main_area = False
    resizing_enabled = False

    def __init__(self):
        super().__init__()

        #----------------------------------------------------------------------
        # User interface...

        self.label = gui.widgetLabel(self.controlArea, "No input yet.")

    @Inputs.integer
    def set_int(self, input_number):
        """Set the input integer."""
        if input_number is None:
            self.label.setText("No input yet.")
        else:
            self.label.setText("The number is %i" % input_number)


# The following code lets you execute the code outside of Orange (to view the
# resulting interface)...
if __name__ == "__main__":
    WidgetPreview(DisplayInt).run(set_int=50)

