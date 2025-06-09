from PySide6.QtCore import QFile, Slot, Qt
from PySide6.QtUiTools import QUiLoader
from viewmodel.viewmodel import ViewModel


class MainWindow:

    def __init__(self):
        # Load the UI file
        self.ui_file = QFile("view/pokergame.ui")
        self.ui_file.open(QFile.OpenModeFlag.ReadOnly)

        # Create a loader and load the UI
        self.loader = QUiLoader()
        self.main_window = self.loader.load(self.ui_file)
        self.ui_file.close()

        self.viewmodel = ViewModel()

        # Connect UI signals to ViewModel slots
        self.main_window.pushButtonAddPlayer.clicked.connect(self.handle_add_player)
        self.main_window.pushButtonDelPlayer.clicked.connect(self.handle_del_player)
        self.main_window.checkBoxDrawGame.toggled.connect(self.handle_draw_game)
        self.main_window.pushButtonDeal.clicked.connect(self.handle_deal_cards)

        # Connect ViewModel signals to UI slots/updates
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.player_removed.connect(self.on_player_deleted)
        self.viewmodel.error_occurred.connect(self.on_error)
        self.viewmodel.game_state_changed.connect(self.update_game_status)

        self.update_game_status("Game setup in progress")

    def show(self):
        self.main_window.show()

    def show_dealt_dialog(self):
        ui_file = QFile("view/cardsdealt.ui")
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    def show_cannot_modify_game_dialog(self):
        ui_file = QFile("view/cannotmodifygame.ui")
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    @Slot()
    def handle_add_player(self):
        if self.viewmodel.check_game_state() in ["playing", "finished"]:
            self.show_cannot_modify_game_dialog()
        else:
            player_name = self.main_window.textEditPlayer.toPlainText().strip()
            self.viewmodel.add_player(player_name)
            self.main_window.textEditPlayer.setFocus()

    @Slot(str)
    def handle_del_player(self):
        if self.viewmodel.check_game_state() in ["playing", "finished"]:
            self.show_cannot_modify_game_dialog()
        else:
            selected_items = self.main_window.listWidgetPlayers.selectedItems()
            for item in selected_items:
                player_name = item.text()
                self.viewmodel.remove_player(player_name)

    @Slot(str)
    def on_player_added(self, player_name: str):
        self.main_window.listWidgetPlayers.addItem(player_name)
        self.main_window.textEditPlayer.clear()

    @Slot(str)
    def on_player_deleted(self, player_name):
        items = self.main_window.listWidgetPlayers.findItems(player_name, Qt.MatchExactly)
        if items:  # if any items were found
            item = items[0]  # take the first (and should be only) item
            row = self.main_window.listWidgetPlayers.row(item)
            self.main_window.listWidgetPlayers.takeItem(row)

    @Slot()
    def handle_draw_game(self):
        if self.viewmodel.check_game_state() in ["playing", "finished"]:
            self.show_cannot_modify_game_dialog()
        else:
            self.viewmodel.set_draw_game(self.main_window.checkBoxDrawGame.isChecked())

    @Slot()
    def handle_deal_cards(self):
        if self.viewmodel.check_game_state() in ["playing", "finished"]:
            self.show_cannot_modify_game_dialog()
        else:
            self.viewmodel.deal()
            self.show_dealt_dialog()

    @Slot(str)
    def update_game_status(self, text: str):
        self.main_window.labelGameStatus.setText(text)

    @Slot(str)
    def on_error(self, error_message: str):
        # For now, just print the error. Later we can add a proper error display
        print(f"Error: {error_message}")
