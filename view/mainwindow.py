from PySide6.QtCore import QFile, Slot, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from viewmodel.viewmodel import ViewModel
import os


class MainWindow:

    def __init__(self):
        # Load the UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui_file = QFile(os.path.join(current_dir, "pokergame.ui"))
        self.ui_file.open(QFile.OpenModeFlag.ReadOnly)

        # Create a loader, load the UI, and lock window size
        self.loader = QUiLoader()
        self.main_window = self.loader.load(self.ui_file)
        self.main_window.setFixedSize(self.main_window.size())
        self.ui_file.close()

        self.viewmodel = ViewModel()

        # Connect UI signals to ViewModel slots
        self.main_window.pushButtonAddPlayer.clicked.connect(self.handle_add_player)
        self.main_window.pushButtonDelPlayer.clicked.connect(self.handle_del_player)
        self.main_window.pushButtonPlayGame.clicked.connect(self.handle_play_game)
        self.main_window.pushButtonRevealWinner.clicked.connect(self.handle_reveal_winner)

        # Connect ViewModel signals to UI slots/updates
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.player_removed.connect(self.on_player_removed)
        self.viewmodel.show_hand_requested.connect(self.on_show_hand_requested)
        self.viewmodel.show_draw_hand_requested.connect(self.on_show_draw_hand_requested)
        self.viewmodel.cards_exchanged.connect((self.on_cards_exchanged))
        self.viewmodel.winner_declared.connect(self.on_winner_declared)
        self.viewmodel.game_state_changed.connect(self.on_game_state_changed)
        self.viewmodel.error_occurred.connect(self.on_error)

        # Connect the restart action
        self.main_window.actionRestart.triggered.connect(self.handle_restart)

        self.on_game_state_changed("Game setup in progress")

    def show(self):
        self.center_dialog(self.main_window)
        self.main_window.show()

    """
    Dialog Box Section
    Contains methods for displaying various dialog boxes used in the game UI
    """

    def center_dialog(self, dialog):
        screen = QApplication.instance().primaryScreen().availableGeometry()
        x = (screen.width() - dialog.width()) // 2
        y = (screen.height() - dialog.height()) // 2
        dialog.move(x, y)

    def show_dealt_dialog(self, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "cardsdealt.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        dialog.labelPlayer.setText(name)

        def show_hand_dialog_chooser():
            if self.viewmodel.get_game_state() == "drawreveal":
                # The lambda is used to pass the name to the show_hand method without calling it immediately
                self.viewmodel.show_hand(name)
            elif self.main_window.checkBoxDrawGame.isChecked():
                self.viewmodel.set_game_state("drawreveal")
                self.viewmodel.show_draw_hand(name)
            else:
                self.viewmodel.show_hand(name)

        dialog.pushButtonShowCards.clicked.connect(show_hand_dialog_chooser)
        dialog.pushButtonDone.clicked.connect(dialog.close)
        ui_file.close()
        self.center_dialog(dialog)
        dialog.exec()

    def show_display_string_dialog(self, text):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "displaystring.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        dialog = self.loader.load(ui_file)
        dialog.labelDisplayString.setText(text)
        dialog.pushButtonClose.clicked.connect(dialog.accept)
        ui_file.close()
        self.center_dialog(dialog)
        dialog.exec()

    def show_hand_dialog(self, hand_list: list):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "hand.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)

        # Best hand and cards to dialog
        dialog = self.loader.load(ui_file)
        dialog.labelHand.setText(hand_list[0])
        dialog.labelCard_1.setText(hand_list[1])
        dialog.labelCard_2.setText(hand_list[2])
        dialog.labelCard_3.setText(hand_list[3])
        dialog.labelCard_4.setText(hand_list[4])
        dialog.labelCard_5.setText(hand_list[5])

        dialog.pushButtonDone.clicked.connect(dialog.close)

        ui_file.close()
        self.center_dialog(dialog)
        dialog.exec()

    def show_draw_hand_dialog(self, player, hand_list: list):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = QFile(os.path.join(current_dir, "drawhand.ui"))
        ui_file.open(QFile.OpenModeFlag.ReadOnly)

        # Best hand and cards to dialog
        dialog = self.loader.load(ui_file)
        dialog.labelHand.setText(hand_list[0])
        dialog.labelCard_1.setText(hand_list[1])
        dialog.labelCard_2.setText(hand_list[2])
        dialog.labelCard_3.setText(hand_list[3])
        dialog.labelCard_4.setText(hand_list[4])
        dialog.labelCard_5.setText(hand_list[5])

        def on_exchange():
            selected_cards = []
            if dialog.groupBox_1.isChecked():
                selected_cards.append(dialog.labelCard_1.text())
            if dialog.groupBox_2.isChecked():
                selected_cards.append(dialog.labelCard_2.text())
            if dialog.groupBox_3.isChecked():
                selected_cards.append(dialog.labelCard_3.text())
            if dialog.groupBox_4.isChecked():
                selected_cards.append(dialog.labelCard_4.text())
            if dialog.groupBox_5.isChecked():
                selected_cards.append(dialog.labelCard_5.text())
            self.viewmodel.exchange_cards(player, selected_cards)
            dialog.close()

        dialog.pushButtonExchange.clicked.connect(on_exchange)

        ui_file.close()
        self.center_dialog(dialog)
        dialog.exec()

    """
    Handle UI Signals Section
    Contains methods that call ViewModel methods in response to UI signals
    """

    @Slot()
    def handle_add_player(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_display_string_dialog("You cannot add/remove players or deal during a game!")
        if self.viewmodel.get_game_state() == "reveal":
            self.show_display_string_dialog("Click the Reveal Winner buton")
        elif self.viewmodel.get_game_state() == "finished":
            self.show_display_string_dialog("Game Over! To restart click Game -> Restart")
        else:
            player_name = self.main_window.textEditPlayer.toPlainText().strip()
            self.viewmodel.add_player(player_name)
            self.main_window.textEditPlayer.setFocus()

    @Slot()
    def handle_del_player(self):
        if self.viewmodel.get_game_state() == "playing":
            self.show_display_string_dialog("You cannot add/remove players or deal during a game!")
        if self.viewmodel.get_game_state() == "reveal":
            self.show_display_string_dialog("Click the Reveal Winner buton")
        elif self.viewmodel.get_game_state() == "finished":
            self.show_display_string_dialog("Game Over! To restart click Game -> Restart")
        else:
            selected_items = self.main_window.listWidgetPlayers.selectedItems()
            for item in selected_items:
                name = item.text()
                self.viewmodel.remove_player(name)

    @Slot()
    def handle_draw_game(self):
        self.viewmodel.set_game_of_draw(self.main_window.checkBoxDrawGame.isChecked())

    @Slot()
    def handle_play_game(self):
        if self.viewmodel.get_game_state() == "setup":
            self.show_display_string_dialog("Must add at least two players to play")
        elif self.viewmodel.get_game_state() == "playing":
            self.show_display_string_dialog("You cannot add/remove players during a game!")
        elif self.viewmodel.get_game_state() == "reveal":
            self.show_display_string_dialog("Click the Reveal Winner button")
        elif self.viewmodel.get_game_state() == "finished":
            self.show_display_string_dialog("Game Over! To restart click Game -> Restart")
        else:
            # Game state is "ready"
            self.viewmodel.deal_cards()

            for i in range(self.main_window.listWidgetPlayers.count()):
                item = self.main_window.listWidgetPlayers.item(i)
                name = item.text()
                # set to reveal for each player since status may be drawgame
                self.viewmodel.set_game_state("reveal")
                self.show_dealt_dialog(name)
            self.viewmodel.game_state_changed.emit("Ready to reveal winner")

    @Slot()
    def handle_reveal_winner(self):
        if self.viewmodel.get_game_state() in ["reveal", "drawreveal"]:
            self.viewmodel.get_winner()
            self.viewmodel.set_game_state("finished")
            self.viewmodel.game_state_changed.emit("Game over")
        elif self.viewmodel.get_game_state() == "finished":
            self.viewmodel.get_winner()
        else:
            self.show_display_string_dialog("You must finish the game first")

    @Slot()
    def handle_restart(self):
        self.viewmodel.restart_game()
        self.main_window.textEditPlayer.clear()
        self.main_window.checkBoxDrawGame.setChecked(False)
        self.main_window.checkBoxDrawGame.setEnabled(True)

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
    def on_show_hand_requested(self, hand_list):
        self.show_hand_dialog(hand_list)

    @Slot(str)
    def on_show_draw_hand_requested(self, player, hand_list):
        self.show_draw_hand_dialog(player, hand_list)

    @Slot(object)
    def on_cards_exchanged(self, hand_list):
        self.show_hand_dialog(hand_list)

    @Slot()
    def on_winner_declared(self, winner):
        self.show_display_string_dialog(winner)

    @Slot(str)
    def on_game_state_changed(self, text):
        self.main_window.statusBar().showMessage(text)
        self.update_checkbox_state()

    @Slot(str)
    def on_error(self, error_message: str):
        self.show_display_string_dialog(error_message)

    # Add this method to update checkbox state based on game state
    def update_checkbox_state(self):
        game_state = self.viewmodel.get_game_state()
        if game_state in ["playing", "reveal", "finished"]:
            self.main_window.checkBoxDrawGame.setEnabled(False)
        else:
            self.main_window.checkBoxDrawGame.setEnabled(True)
