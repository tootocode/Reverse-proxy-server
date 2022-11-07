# coding=utf-8
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *

from Scanner import Ui_Login_Window  # 由.UI文件生成.py文件后，导入创建的GUI类
from Scanner.mainpage import MainWindow


# QtWidgets.QMainWindow：继承该类方法
class Login_window(QtWidgets.QMainWindow, Ui_Login_Window.LoginForm):

    # __init__: 析构函数，也就是类被创建后就会预先加载的项目。
    # 马上运行，这个方法可以用来对你的对象做一些你希望的初始化。
    def __init__(self, Ui_Main):
        # 这里需要重载一下Login_window，同时也包含了QtWidgets.QMainWindow的预加载项。
        super(Login_window, self).__init__()
        # self.setupUi(self)
        self.Ui_Main = Ui_Main
        # 将点击事件与槽函数进行连接
        self.btn_login.clicked.connect(self.btn_login_fuc)
        # self.lbl_logo.move(100, 100)

        # 登录按钮 函数

    def btn_login_fuc(self):
        # 1 获取输入的账户和密码
        account = self.led_workerid.text()  # 记得text要打括号（）！
        password = self.led_pwd.text()
        if account == "" or password == "":
            reply = QMessageBox.warning(self, "警告", "账号密码不能为空，请输入！")
            return

        # 2 查询数据库，判定是否有匹配
        # ms = MSSQL()
        # result = ms.Login_result(account, password)
        if account == "admin" and password == "admin":

            # # 1打开新窗口
            self.Ui_Main.show()
            # # 2关闭本窗口

            self.close()

            # return 'login success'
        else:
            reply = QMessageBox.warning(self, "警告", "账户或密码错误，请重新输入！")

# if __name__ == '__main__':  # 如果这个文件是主程序。
#     app = QtWidgets.QApplication(sys.argv)  # QApplication相当于main函数，也就是整个程序（很多文件）的主入口函数。对于GUI程序必须至少有一个这样的实例来让程序运行。
#     window = Login_window()  # 生成一个实例（对象）
#     Ui_Main = MainWindow(1)  # 生成主窗口的实例
#     window.show()  # 有了实例，就得让它显示。这里的show()是QWidget的方法，用来显示窗口。
#     sys.exit(app.exec_())  # 调用sys库的exit退出方法，条件是app.exec_()也就是整个窗口关闭。
