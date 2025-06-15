from PySide6.QtCore import QFile, Slot, Qt
from PySide6.QtUiTools import QUiLoader
from viewmodel.viewmodel import ViewModel
import os


class MainWindow:

    def __init__(self):
        # Load the UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui_file = QFile(os.path.join(current_dir, "pokergame.ui"))
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
        self.main_window.pushButtonPlayGame.clicked.connect(self.handle_play_game)
        self.main_window.pushButtonRevealWinner.clicked.connect(self.handle_reveal_winner)

        # Connect ViewModel signals to UI slots/updates
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.player_removed.connect(self.on_player_removed)
        self.viewmodel.show_hand_requested.connect(self.on_show_hand_requested)
        self.viewmodel.winner_declared.connect(self.on_winner_declared)
        self.viewmodel.winner_set_requested.connect(self.on_winner_set_requested)
        self.viewmodel.game_state_changed.connect(self.on_game_state_changed)
        self.viewmodel.error_occurred.connect(self.on_error)

        # Connect the restart action
        self.main_window.actionRestart.triggered.connect(self.handle_restart)

        self.on_game_state_changed("Game setup in progress")

    def show(self):
        self.main_window.show()

    """
    Dialog Box Section
    Contains methods for displaying various dialog boxes used in the game UI
    """

    def show_cannot_modify_game_dialog(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "cannotmodifygame.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    def show_no_hand_to_show_dialog(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "nohandtoshow.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    def show_dealt_dialog(self, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "cardsdealt.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)

        dialog.labelPlayer.setText(name)
        # Create a lambda function to capture the name parameter
        # (otherwise show_hand would be executed immediately)
        dialog.pushButtonShowCards.clicked.connect(lambda: self.viewmodel.show_hand(name))
        dialog.pushButtonDone.clicked.connect(dialog.close)
        ui_file.close()
        dialog.exec()

    def show_show_cards_ui(self, hand):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "showcards.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        dialog.labelShowCards.setText(hand)
        ui_file.close()
        dialog.exec()

    def show_declare_winner_dialog(self, text):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "declarewinner.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        dialog.labelWinner.setText(text)
        ui_file.close()
        dialog.exec()

    def show_cannot_reveal_winner_dialog(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "cannotrevealwinner.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    def show_game_over_dialog(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "gameover.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        ui_file.close()
        dialog.exec()

    """
    Handle UI Signals Section
    Contains methods that call ViewModel methods in response to UI signals
    """

    @Slot()
    def handle_add_player(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_cannot_modify_game_dialog()
        elif self.viewmodel.get_game_state() == "finished":
            self.show_game_over_dialog()
        else:
            player_name = self.main_window.textEditPlayer.toPlainText().strip()
            self.viewmodel.add_player(player_name)
            self.main_window.textEditPlayer.setFocus()

    @Slot()
    def handle_del_player(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_cannot_modify_game_dialog()
        elif self.viewmodel.get_game_state() == "finished":
            self.show_game_over_dialog()
        else:
            selected_items = self.main_window.listWidgetPlayers.selectedItems()
            for item in selected_items:
                name = item.text()
                self.viewmodel.remove_player(name)

    @Slot()
    def handle_draw_game(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_cannot_modify_game_dialog()
        elif self.viewmodel.get_game_state() == "finished":
            self.show_game_over_dialog()
        else:
            self.viewmodel.set_game_of_draw(self.main_window.checkBoxDrawGame.isChecked())

    @Slot()
    def handle_play_game(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_cannot_modify_game_dialog()
        elif self.viewmodel.get_game_state() == "finished":
            self.show_game_over_dialog()
        else:
            self.viewmodel.deal_cards()

            for i in range(self.main_window.listWidgetPlayers.count()):
                item = self.main_window.listWidgetPlayers.item(i)
                name = item.text()
                self.show_dealt_dialog(name)
            self.viewmodel.set_game_state("reveal")
            self.viewmodel.game_state_changed.emit("Ready to reveal winner")

    @Slot()
    def handle_reveal_winner(self):
        if self.viewmodel.get_game_state() == "reveal":
            self.viewmodel.get_winner()
            self.viewmodel.set_game_state("finished")
            self.viewmodel.game_state_changed.emit("Game over")
        else:
            self.show_cannot_reveal_winner_dialog()

    @Slot()
    def handle_restart(self):
        """Handle the restart action from the menu."""
        self.viewmodel.restart_game()
        self.main_window.listWidgetPlayers.clear()
        self.main_window.textEditPlayer.clear()
        self.main_window.checkBoxDrawGame.setChecked(False)

    """
    On Receiving ViewModel Signals Section
    Contains methods to update UI
    """

    @Slot(str)
    def on_player_added(self, player_name: str):
        self.main_window.listWidgetPlayers.addItem(player_name)
        self.main_window.textEditPlayer.clear()

    @Slot(str)
    def on_player_removed(self, player_name):
        items = self.main_window.listWidgetPlayers.findItems(player_name, Qt.MatchExactly)
        if items:  # if any items were found
            item = items[0]  # take the first (and should be only) item
            row = self.main_window.listWidgetPlayers.row(item)
            self.main_window.listWidgetPlayers.takeItem(row)

    @Slot(str)
    def on_show_hand_requested(self, hand):
        self.show_show_cards_ui(hand)

    @Slot()
    def on_winner_declared(self, text):
        self.show_declare_winner_dialog(text)

    @Slot()
    def on_winner_set_requested(self, winner_set):
        pass

    @Slot(str)
    def on_game_state_changed(self, text):
        self.main_window.labelGameStatus.setText(text)

    @Slot(str)
    def on_error(self, error_message: str):
        # For now, just print the error. Later we can add a proper error display
        print(f"Error: {error_message}")
