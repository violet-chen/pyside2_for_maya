# coding:utf-8
# 自定义颜色按钮(使用maya的颜色选择窗口)
from functools import partial
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CustomColorButton(QtWidgets.QWidget): # 自定义颜色按钮

    color_changed = QtCore.Signal(QtGui.QColor) # 自定义信号

    def __init__(self, color=QtCore.Qt.white, parent=None): # 表示可以类接收一个颜色参数,默认是白色
        super(CustomColorButton, self).__init__(parent)

        self.setObjectName("CustomColorButton")

        self.create_control()

        self.set_size(50, 14)
        self.set_color(color) # 设置初始颜色,如果对象有传过来颜色设置则为对象的颜色

    def create_control(self):
        """ 1. 创建colorSliderGrp """
        window = cmds.window()
        self._name = cmds.colorSliderGrp()
        # print("original name: {0}".format(self._name))

        """ 2. 找到colorSliderGrp控件 """
        color_slider_obj = omui.MQtUtil.findControl(self._name) # color_slider_obj是一个c++的形式
        if color_slider_obj:
            self._color_slider_widget = wrapInstance(long(color_slider_obj), QtWidgets.QWidget)
        
            """ 3. 将colorSliderGrp控件的父级设置为这个自定义控件 """
            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setObjectName("main_layout")
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self._color_slider_widget)

            """ 4. 更新colorSliderGrp的control name (之前是属于maya的) """
            self._name = self._color_slider_widget.objectName()
            # print("new name: {0}".format(self._name))

            """ 5. 识别或存储 colorSliderGrp的子控件(在必要的时候可以隐藏它) """
            # children = self._color_slider_widget.children()
            # for child in children:
            #     print(child)
            #     print(child.objectName())
            # print("---")

            self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
            if self._slider_widget:
                self._slider_widget.hide()
            
            self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")

            cmds.colorSliderGrp(self._name, e=True, changeCommand=partial(self.on_color_changed))

        cmds.deleteUI(window, window=True)
          
    
    def set_size(self, width, height):
        self._color_slider_widget.setFixedWidth(width)
        self._color_widget.setFixedHeight(height)
    
    def set_color(self, color):
        color = QtGui.QColor(color)

        if color != self.get_color():
            cmds.colorSliderGrp(self._name, e=True, rgbValue=(color.redF(), color.greenF(), color.blueF())) # F代表以浮点数表示
            self.on_color_changed()
    
    def get_color(self):
        color = cmds.colorSliderGrp(self._name, q=True, rgbValue=True)

        color = QtGui.QColor(color[0] *255, color[1] * 255, color[2] * 255)
        return color
      
    def on_color_changed(self, *args):
        self.color_changed.emit(self.get_color())

class TestDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Embedding Maya Controls"

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(320, 150)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        window_name = "WindowName"
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)
        self.setObjectName(window_name)

        self.foreground_color = QtCore.Qt.white
        self.background_color = QtCore.Qt.black

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """ 控件 """
        self.foreground_color_btn = CustomColorButton(QtCore.Qt.white) # 自定义的颜色按钮
        self.background_color_btn = CustomColorButton(QtCore.Qt.black) # 自定义的颜色按钮

        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layouts(self):
        """ 布局 """
        color_layout = QtWidgets.QFormLayout()
        color_layout.addRow("Foreground:", self.foreground_color_btn)
        color_layout.addRow("Background:", self.background_color_btn)

        color_grp = QtWidgets.QGroupBox("Color Options")
        color_grp.setObjectName("colorGrp")
        color_grp.setLayout(color_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.addWidget(color_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def create_connections(self):
        """ 信号与槽的连接 """
        self.foreground_color_btn.color_changed.connect(self.on_foreground_color_changed)
        self.background_color_btn.color_changed.connect(self.on_background_color_changed)

        self.close_btn.clicked.connect(self.close)
    
    def on_foreground_color_changed(self, new_color):
        print("New foreground color: ({0}, {1}, {2})".format(new_color.red(), new_color.green(), new_color.blue()))
    
    def on_background_color_changed(self, new_color):
        print("New background color: ({0}, {1}, {2})".format(new_color.red(), new_color.green(), new_color.blue()))

if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
