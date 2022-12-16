# coding:utf-8
# 自定义信号
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def maya_main_window():
    # 将maya主窗口的C++指针转换为python可以接受的对象。
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class MyLineEdit(QtWidgets.QLineEdit):
    enter_pressed = QtCore.Signal(str)  # 新建自定义信号

    def keyPressEvent(self, e):  # 使用QLineEdit自带的事件，当按键按下时触发并发送数据
        super(MyLineEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter:
            self.enter_pressed.emit("Enter Key Pressed")  # 当右enter键按下时发送数据
        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Return Key Pressed") # 当回车键按下时发送数据

class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle('Test Dialog')
        self.setMinimumWidth(200)
        self.setMinimumHeight(90)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)  # 将maya窗口的问号标志排除掉

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.lineEdit = MyLineEdit()  # MyLineEdit 是自定义的继承QtWidgets.QLineEdit的类
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Name:", self.lineEdit)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)  # 传递self将这个layout作为主layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.lineEdit.enter_pressed.connect(self.on_enter_pressed)
        self.cancel_btn.clicked.connect(self.close)  # self.close是自带的不需要自己写函数

    def on_enter_pressed(self, text):
        print(text)


if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
