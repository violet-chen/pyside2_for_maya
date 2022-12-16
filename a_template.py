# coding:utf-8
import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance
from maya import OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


class TestDialog(QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle('MAYA-2018')
        self.setMinimumSize(300, 80)
        self.setWindowFlags(Qt.WindowType.Window)
        window_name = "WindowName"
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)
        self.setObjectName(window_name)
        self.setStyleSheet("font: 12pt 'Arial';")

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """ 控件 """
        pass

    def create_layouts(self):
        """ 布局 """
        pass

    def create_connections(self):
        """ 信号与槽的连接 """
        pass



def main():
    global aa
    app = qApp if QApplication.instance() else QApplication([])
    aa = TestDialog()
    aa.show()
    app.exec_()
