# coding:utf-8
# 自定义颜色按钮
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CustomColorButton(QtWidgets.QLabel): # 扩展QLabel的内容

    color_changed = QtCore.Signal() # 自定义信号

    def __init__(self, color=QtCore.Qt.white, parent=None): # 表示可以类接收一个颜色参数,默认是白色
        super(CustomColorButton, self).__init__(parent)

        self._color = QtGui.QColor() # _开头表示私有变量,表面希望通过函数获取与更改这个变量

        self.set_size(50, 14)
        self.set_color(color) # 设置初始颜色,如果对象有传过来颜色设置则为对象的颜色
    
    def set_size(self, width, height):
        self.setFixedSize(width, height)
    
    def set_color(self, color):
        color = QtGui.QColor(color)

        if self._color != color:
            self._color = color
            
            pixmap = QtGui.QPixmap(self.size())
            pixmap.fill(self._color)
            self.setPixmap(pixmap)

            self.color_changed.emit() # 如果执行到这里，就发送信号传递给槽函数并执行
    
    def get_color(self):
        return self._color
    
    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, options=QtWidgets.QColorDialog.DontUseNativeDialog) # 颜色对话框
        if color.isValid():
            self.set_color(color)
    
    def mouseReleaseEvent(self, mouse_event):
        if mouse_event.button() == QtCore.Qt.LeftButton:
            self.select_color()

class TestDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Custom Color Example"

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(320, 150)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        window_name = "WindowName"
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)
        self.setObjectName(window_name)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """ 控件 """
        self.foreground_color_btn = CustomColorButton(QtCore.Qt.white) # 自定义的颜色按钮
        self.background_color_btn = CustomColorButton(QtCore.Qt.black) # 自定义的颜色按钮

        self.print_btn = QtWidgets.QPushButton("Print")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layouts(self):
        """ 布局 """
        color_layout = QtWidgets.QFormLayout()
        color_layout.addRow("Foreground:", self.foreground_color_btn)
        color_layout.addRow("Background:", self.background_color_btn)

        color_grp = QtWidgets.QGroupBox("Color Options")
        color_grp.setLayout(color_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.print_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.addWidget(color_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def create_connections(self):
        """ 信号与槽的连接 """
        self.foreground_color_btn.color_changed.connect(self.print_colors)
        self.background_color_btn.color_changed.connect(self.print_colors)

        self.print_btn.clicked.connect(self.print_colors)
        self.close_btn.clicked.connect(self.close)
    
    def print_colors(self):
        fg_color = self.foreground_color_btn.get_color()
        bg_color = self.background_color_btn.get_color()

        print("Foreground Color: [{0}, {1}, {2}]".format(fg_color.red(),fg_color.green(),fg_color.blue()))
        print("Background Color: [{0}, {1}, {2}]".format(bg_color.red(),bg_color.green(),bg_color.blue()))

if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
