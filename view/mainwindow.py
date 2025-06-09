from PySide6.QtCore import QFile, Slot, Qt
from PySide6.QtUiTools import QUiLoader
from viewmodel.viewmodel import ViewModel


class MainWindow:
    def __init__(self):
        # Load the UI file
        ui_file = QFile("view/pokergame.ui")
        ui_file.open(QFile.ReadOnly)

        # Create a loader and load the UI
        loader = QUiLoader()
        self.main_window = loader.load(ui_file)
        ui_file.close()

        self.viewmodel = ViewModel()

        # Connect UI signals to ViewModel slots
        self.main_window.pushButtonAddPlayer.clicked.connect(self.handle_add_player)
        self.main_window.pushButtonDelPlayer.clicked.connect(self.handle_del_player)
        self.main_window.checkBoxDrawGame.toggled.connect(self.handle_draw_game)

        # Connect ViewModel signals to UI slots/updates
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.player_removed.connect(self.on_player_removed)
        self.viewmodel.error_occurred.connect(self.on_error)

    def show(self):
        self.main_window.show()

    @Slot()
    def handle_add_player(self):
        player_name = self.main_window.textEditPlayer.toPlainText().strip()
        self.viewmodel.add_player(player_name)

    @Slot(str)
    def handle_del_player(self):
        selected_items = self.main_window.listWidgetPlayers.selectedItems()
        for item in selected_items:
            player_name = item.text()
            self.viewmodel.remove_player(player_name)

    @Slot(str)
    def on_player_added(self, player_name: str):
        self.main_window.listWidgetPlayers.addItem(player_name)
        self.main_window.textEditPlayer.clear()

    @Slot(str)
    def on_player_removed(self, player_name):
        items = self.main_window.listWidgetPlayers.findItems(
            player_name, Qt.MatchExactly
        )
        if items:  # if any items were found
            item = items[0]  # take the first (and should be only) item
            row = self.main_window.listWidgetPlayers.row(item)
            self.main_window.listWidgetPlayers.takeItem(row)

    @Slot()
    def handle_draw_game(self):
        self.viewmodel.set_draw_game(self.main_window.checkBoxDrawGame.isChecked())

    @Slot(str)
    def on_error(self, error_message: str):
        # For now, just print the error. Later we can add a proper error display
        print(f"Error: {error_message}")
