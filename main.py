from sys import argv, exit
from app import App
from PyQt5.QtWidgets import QApplication
from utils import main_style


if __name__ == "__main__":

    q_application = QApplication(argv)
    app = App()

    q_application.setStyleSheet(main_style)
    app.show()

    exit(q_application.exec())
