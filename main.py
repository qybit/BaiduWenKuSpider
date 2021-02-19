import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from WenKuDownload import *
import os


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    try:
        os.environ["CUDA_VISIBLE_DEVICES"] = "2"
        app = QApplication(sys.argv)
        myWin = MyWindow()
        myWin.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
