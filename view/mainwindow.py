from PySide6.QtCore import Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from viewmodel.viewmodel import PokerGameViewModel


class MainWindow:
    def __init__(self):
        # Load the UI file
        ui_file = QFile("view/pokergame.ui")
        ui_file.open(QFile.ReadOnly)
        
        # Create a loader and load the UI
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        
        # Create and set up the ViewModel
        self.viewmodel = PokerGameViewModel()
        
        # Connect UI signals to ViewModel slots
        self.window.pushButton.clicked.connect(self.handle_add_player)
        
        # Connect ViewModel signals to UI updates
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.error_occurred.connect(self.on_error)
        
    def show(self):
        self.window.show()
        
    @Slot()
    def handle_add_player(self):
        player_name = self.window.textEdit.toPlainText().strip()
        self.viewmodel.add_player(player_name)
        
    @Slot(str)
    def on_player_added(self, player_name: str):
        self.window.listWidget.addItem(player_name)
        self.window.textEdit.clear()
        
    @Slot(str)
    def on_error(self, error_message: str):
        # For now, just print the error. Later we can add a proper error display
        print(f"Error: {error_message}")
