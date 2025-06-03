from PySide6.QtCore import QObject, Signal, Slot


class MyModel(QObject):
    data_changed = Signal(str)

    def update_data(self, value):
        # Imagine some internal update here
        self.data_changed.emit(value)


class MyViewModel(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.data_changed.connect(self.on_model_data_changed)

    @Slot(str)
    def on_model_data_changed(self, value):
        print(f"ViewModel received update: {value}")
        # Forward this to view or process it


class MyView(QObject):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

    def user_input(self, new_value):
        self.view_model.model.update_data(new_value)


# Wiring it together
model = MyModel()
view_model = MyViewModel(model)
view = MyView(view_model)

view.user_input("Hello MVVM")
