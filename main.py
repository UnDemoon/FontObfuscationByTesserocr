# 这是一个示例 Python 脚本。
import os
import sys
import time
import tools
from ui_home import Ui_MainWindow as Ui
from PyQt5 import QtWidgets, QtCore, QtGui
from Decoder import Decoder, OCR


#   ui
class MyApp(QtWidgets.QMainWindow, Ui):
    def __init__(self):
        #   ui初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui.__init__(self)
        self.setupUi(self)
        self.__uiCustom()

        '''ui自定义补充'''

    def __uiCustom(self):
        self.pushButton_2.clicked.connect(self.open_file)  # 搜索

    def open_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_name:
            self.lineEdit.setText(file_name)
            self.ocr_file(file_name)

    def ocr_file(self, file_path):
        html_txt = tools.readHtml(file_path)
        font_file = tools.getFontFile(file_path)
        d = Decoder('tessdata-main/', font_file)
        txt = ''.join(map(d.decode, html_txt))
        self.textEdit.setText(txt if txt else '')


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
