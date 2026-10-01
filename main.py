# Лабораторная работа №3 - Часть 2 - MVC

import sys
from PyQt5.QtWidgets import QApplication
from visual import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
