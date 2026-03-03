# Standard imports...
from Orange.widgets import widget, gui, utils
from Orange.widgets.utils.widgetpreview import WidgetPreview

__version__ = "0.01"


class Add(widget.OWWidget):
    """An Orange widget that adds two numbers"""

    #----------------------------------------------------------------------
    # Widget's metadata...

    name = "Add"
    description = "Add two numbers"
    icon = "icons/mywidget.svg"
    priority = 20

    #----------------------------------------------------------------------
    # Channel definitions...

    inputs = [
        ("A", int, "set_A"),
        ("B", int, "set_B"),
    ]
    outputs = [("Addition result", int)]

    #----------------------------------------------------------------------
    # GUI layout parameters...

    want_main_area = False
    resizing_enabled = False

    def __init__(self):
        super().__init__()

        self.a = None
        self.b = None
        
        #----------------------------------------------------------------------
        # User interface...

        self.label = gui.widgetLabel(self.controlArea, "2 inputs are needed.")

    def set_A(self, a):
        """Set the input 'A'."""
        self.a = a

    def set_B(self, b):
        """Set the input 'B'."""
        self.b = b

    def handleNewSignals(self):
        """Reimplemented from OWWidget."""
        if self.a is not None and self.b is not None:
            result = self.a + self.b
            self.label.setText("%i + %i = %i" % (self.a, self.b, result))
            self.send("Addition result", self.a + self.b)
        else:
            self.label.setText("2 inputs are needed.")
            # Clear the channel by sending None.
            self.send("Addition result", None)
 
 
# The following code lets you execute the code outside of Orange (to view the
# resulting interface)...
if __name__ == "__main__":
    WidgetPreview(Add).run(set_A=20, set_B=30)

