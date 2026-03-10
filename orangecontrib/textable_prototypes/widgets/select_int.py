# Standard imports...
from Orange.widgets import widget, gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Input, Output


__version__ = "0.01"


class SelectInt(widget.OWWidget):
    """An Orange widget that lets the user select an integer value"""

    #----------------------------------------------------------------------
    # Widget's metadata...

    name = "Select Integer"
    description = "Select an integer value"
    icon = "icons/mywidget.svg"
    priority = 10

    #----------------------------------------------------------------------
    # Channel definitions (NB: no input in this case)...
        
    class Outputs():
        integer = Output("Integer", int)

    #----------------------------------------------------------------------
    # GUI layout parameters...

    want_main_area = False
    resizing_enabled = False

    #----------------------------------------------------------------------
    # Settings declaration and initializations (default values)...

    selected_int = Setting(50)

    def __init__(self):
        super().__init__()
        
        #----------------------------------------------------------------------
        # User interface...

        gui.spin(
            widget=self.controlArea,    # Containing interface element (usually
                                        # self.controlArea or some widgetBox).
            master=self,                # Object which stores the corresponding
                                        # setting (normally self).
            value='selected_int',       # Setting name.
            label='Select an integer: ',# Label.
            callback=self.int_changed,  # Method called when control changes.
            tooltip='Select a value between 1 and 100',
            minv=1,                     # The last 3 arguments are specific to
            maxv=100,                   # controls of the "spin" type...
            step=1,
        )

        self.int_changed()

    def int_changed(self):
        """Send the entered number on "Number" output"""
        self.Outputs.integer.send(self.selected_int)
        if self.selected_int :
            self.Outputs.integer.send(self.selected_int)
        else:
            self.Outputs.operation_result.send(None)


# The following code lets you execute the code outside of Orange (to view the
# resulting interface)...
if __name__ == "__main__":
    WidgetPreview(SelectInt).run()

