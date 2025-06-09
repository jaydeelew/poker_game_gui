#! /usr/bin/env python3

from PySide6.QtWidgets import QApplication
from view.mainwindow import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
