import sys
from PyQt6.QtWidgets import QApplication
from lib.controller.screens.app_screen import MainWindow
import qdarktheme

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(qdarktheme.load_stylesheet(theme='auto'))
    main_window = MainWindow()

    # main_window.showMaximized()
    main_window.show()
    sys.exit(app.exec())
