# Standard imports...
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import Input, Output

__version__ = "0.01"


class Operation(widget.OWWidget):
    """An Orange widget that lets the user apply an operation to two numbers"""

    #----------------------------------------------------------------------
    # Widget's metadata...

    name = "Operation"
    description = "Apply an operation to two numbers"
    icon = "icons/mywidget.svg"
    priority = 20

    #----------------------------------------------------------------------
    # Channel definitions...
    class Inputs:
        A = Input("A", int)
        B = Input("B", int)
    
    class Outputs:
        operation_result = Output("Operation result", int)

    #----------------------------------------------------------------------
    # GUI layout parameters...

    want_main_area = False
    resizing_enabled = False

    #----------------------------------------------------------------------
    # Settings declaration and initializations (default values)...

    selected_operation = Setting("+")

    def __init__(self):
        super().__init__()

        self.a = None
        self.b = None
        
        #----------------------------------------------------------------------
        # User interface...

        gui.comboBox(
            widget=self.controlArea,
            master=self,
            value='selected_operation',
            label='Select an operation: ',
            tooltip='+ : addition\n- : subtract\n* : multiply',
            items=['+', '-', '*'],
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
            if self.selected_operation == "+":
                result = self.a + self.b
            elif self.selected_operation == "-":
                result = self.a - self.b
            elif self.selected_operation == "*":
                result = self.a * self.b
            self.label.setText(
                "%i %s %i = %i" % (
                    self.a,
                    self.selected_operation,
                    self.b, 
                    result,
                )
            )
            self.Outputs.operation_result.send(result)
        else:
            self.label.setText("2 inputs are needed.")
            # Clear the channel by sending None.
            self.Outputs.operation_result.send(None)
 
 
# The following code lets you execute the code outside of Orange (to view the
# resulting interface)...
if __name__ == "__main__":
    WidgetPreview(Operation).run(set_A=20, set_B=30)

