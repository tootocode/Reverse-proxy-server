# coding=utf-8
import sys

from PyQt5 import QtWidgets

from Scanner.login import Login_window
from Scanner.mainpage import MainWindow

if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # login = Login_window()
    # login.show()
    # ui = MainWindow(1)
    # login.btn_login.clicked.connect(
    #     lambda: {login.close(), ui.show()}
    # )
    # sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    Ui_Main = MainWindow(1)
    window = Login_window(Ui_Main)

    window.show()
    sys.exit(app.exec_())


