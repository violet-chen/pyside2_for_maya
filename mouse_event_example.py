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


class MoveableWidget(QtWidgets.QWidget):

    def __init__(self, x, y, width, height, color, parent=None):
        super(MoveableWidget, self).__init__(parent)

        self.setFixedSize(width, height)
        self.move(x, y)

        self.color = color
        self.original_color = color

        self.move_enabled = False
    
    def mousePressEvent(self, mouse_event):
        """ 鼠标点击时的事件 """
        print("Mouse Button Pressed")

        if mouse_event.button() == QtCore.Qt.LeftButton:
            self.initial_pos = self.pos()
            self.global_pos = mouse_event.globalPos()

            self.move_enabled = True # 点击时可以移动widget
    
    def mouseReleaseEvent(self, mouse_event):
        """ 鼠标释放时的事件 """
        print("Mouse Button Released")

        if self.move_enabled:
            self.move_enabled = False # 松开后不能移动widget
    
    def mouseDoubleClickEvent(self, mouse_event):
        """ 鼠标双击后改变颜色 """
        print("Mouse Double-Click")

        if self.color == self.original_color:
            self.color = QtCore.Qt.yellow
        else:
            self.color = self.original_color

        self.update() # 更新颜色
    
    def mouseMoveEvent(self, mouse_event):
        """ 鼠标点击并移动时widget也移动 """
        print("Mouse Move")

        if self.move_enabled:
            diff = mouse_event.globalPos() - self.global_pos
            self.move(self.initial_pos + diff)
    
    def paintEvent(self, paint_event):
        """ 绘制填充矩形 """
        painter = QtGui.QPainter(self)
        painter.fillRect(paint_event.rect(), self.color)

class MouseEventExample(QtWidgets.QDialog):

    WINDOW_TITLE = "MAYA-2018"

    def __init__(self, parent=maya_main_window()):
        super(MouseEventExample, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(400, 400)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """ 控件 """
        self.red_widget = MoveableWidget(100, 100, 24, 24, QtCore.Qt.red, self)
        self.blue_widget = MoveableWidget(300, 300, 24, 24, QtCore.Qt.blue, self)

    def create_layouts(self):
        """ 布局 """
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)

if __name__ == '__main__':

    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = MouseEventExample()
    ui.show()
