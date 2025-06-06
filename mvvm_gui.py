from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QObject, Signal, Slot
import sys


class Model(QObject):
    data_changed_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.data = ""

    def update_data(self, value):
        if self.data != value:
            self.data = value
            # Model data has changed, emit signal to notify listeners
            self.data_changed_signal.emit(value)


class ViewModel(QObject):
    data_for_view_signal = Signal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model
        # on_model_data_changed called when data_changed_signal received from model
        self.model.data_changed_signal.connect(self.on_model_data_changed)

    # The str value emitted by view.user_input_signal
    # is passed as arg to this function
    @Slot(str)
    def handle_user_input(self, value):
        # Use a direct method call when the ViewModel
        # is responsible for updating the Model.
        self.model.update_data(value)

    # The str value emitted by model.data_changed_signal
    # is passed as arg to this function
    @Slot(str)
    def on_model_data_changed(self, value):
        # Notify the view via data_for_view_signal
        self.data_for_view_signal.emit(value)


class View(QWidget):
    user_input_signal = Signal(str)

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        # Connect the data_for_view_signal from ViewModel
        # to the update_view (slot method) in View (this object)
        # so that the value of data_for_view_signal is passed to update_view
        # when the signal is received.
        self.view_model.data_for_view_signal.connect(self.update_view)
        # Connect the user_input_signal from View (this object)
        # to the handle_user_input (slot method) in ViewModel
        # so that the value of user_input_signal is passed to handle_user_input
        # when the signal is received.
        self.user_input_signal.connect(self.view_model.handle_user_input)
        self.init_ui()

    def init_ui(self):
        # create a vertical layout
        self.layout = QVBoxLayout()
        # create a line edit widget
        self.input = QLineEdit()
        # create a label widget
        self.label = QLabel("Enter text above")
        # add the line edit and label to the layout
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.label)
        # set the layout to the QWidget
        self.setLayout(self.layout)
        # connect the textChanged signal of the QLineEdit
        # to the on_text_changed slot
        self.input.textChanged.connect(self.on_text_changed)
        # set the window title
        self.setWindowTitle("Simple MVVM Example")

    @Slot(str)
    def on_text_changed(self, text):
        # Emit user input to the ViewModel
        self.user_input_signal.emit(text)

    @Slot(str)
    def update_view(self, value):
        self.label.setText(f"View updated with: {value}")


if __name__ == "__main__":
    # Wiring it together
    # - The view sends user input to the viewmodel.
    # - The viewmodel updates the model.
    # - The model notifies the viewmodel of changes.
    # - The viewmodel notifies the view of changes.
    # Qt Application object creates the event loop
    app = QApplication(sys.argv)
    model = Model()
    view_model = ViewModel(model)
    view = View(view_model)
    # Show the QWidget
    view.show()
    # Start the event loop with app.exec() and exit the program with sys.exit().
    # app.exec() returns the exit code of the application.
    # The return value of app.exec() is passed to sys.exit(),
    # so that the program exits with the return value of app.exec().
    sys.exit(app.exec())
