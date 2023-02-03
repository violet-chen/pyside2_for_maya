# coding:utf-8
import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2 import QtUiTools
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


class DesignerUI(QDialog):

    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)
        
        self.setWindowTitle("Designer UI")

        self.init_ui()
        self.create_layouts()
        self.create_connections()

    def init_ui(self):
        """加载ui文件"""
        f = QFile("C:/Users/Administrator/Desktop/untitled.ui")
        f.open(QFile.ReadOnly)
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self) # designer对象
        
        f.close()

    def create_layouts(self):
        """ 布局 """
        self.ui.layout().setContentsMargins(6, 6, 6, 6)

    def create_connections(self):
        """ 将designer中的控件尽心信号与槽的连接 """
        self.ui.okButton.clicked.connect(self.do_something) 
        self.ui.cancelButton.clicked.connect(self.close)
    
    def do_something(self):
        print("TODO: Do something here")

def main():
    
    try:
        designer_ui.close()
        designer_ui.deleteLater()
    except:
        pass
    
    designer_ui = DesignerUI()
    designer_ui.show()
