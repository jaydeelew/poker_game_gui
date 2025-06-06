from PySide6.QtCore import QObject, Signal, Slot


class Model(QObject):
    data_changed_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.data = ""

    def update_data(self, value):
        if self.data != value:
            self.data = value
            print(
                f"- Model's update_data function was called by \
handle_user_input with: {value}"
            )
            print("- Model emits data_changed_signal from update_data")
            self.data_changed_signal.emit(value)


class ViewModel(QObject):
    data_for_view_signal = Signal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model
        # on_model_data_changed called when data_changed_signal rcvd from model
        self.model.data_changed_signal.connect(self.on_model_data_changed)

    # The str value emitted by view.user_input_signal
    # is passed as arg to this function
    @Slot(str)
    def handle_user_input(self, value):
        print(
            f"- ViewModel's handle_user_input is triggered by \
user_input_signal with: {value}"
        )
        # Use a direct method call when the ViewModel
        # is responsible for updating the Model
        self.model.update_data(value)

    # The str value emitted by model.data_changed_signal
    # is passed as arg to this function
    @Slot(str)
    def on_model_data_changed(self, value):
        print(
            f"- ViewModel's on_model_data_changed is triggered \
by data_changed_signal with: {value}"
        )
        print(f"- ViewModel emits data_for_view_signal with: {value}")
        self.data_for_view_signal.emit(value)  # Notify the view


class View(QObject):
    user_input_signal = Signal(str)

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # This line connects the data_for_view_signal from ViewModel
        # to the update_view (slot method) in View (this object)
        # so that the value of data_for_view_signal is passed to update_view
        # when the signal is received.
        self.view_model.data_for_view_signal.connect(self.update_view)

        # This line connects the user_input_signal from View (this object)
        # to the handle_user_input (slot method) in ViewModel
        # so that the value of user_input_signal is passed to handle_user_input
        # when the signal is received.
        self.user_input_signal.connect(self.view_model.handle_user_input)

    def user_input(self, value):
        print(f"- View emits user_input_signal with: {value}")
        self.user_input_signal.emit(value)

    @Slot(str)
    def update_view(self, value):
        print(
            f"- View's update_view slot is triggered by \
data_for_view_signal with: {value}"
        )


# - The view sends user input to the viewmodel.
# - The viewmodel updates the model.
# - The model notifies the viewmodel of changes.
# - The viewmodel notifies the view of changes.

if __name__ == "__main__":
    model = Model()
    view_model = ViewModel(model)
    view = View(view_model)
    view.user_input("Hello MVVM")
