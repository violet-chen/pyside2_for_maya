# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle('MAYA-2018')
        self.setMinimumSize(300, 80)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
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



if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
