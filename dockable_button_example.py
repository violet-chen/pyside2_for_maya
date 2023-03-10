# coding:utf-8
# 配合MayaQWidgetDockableMixin模块制作 可以停靠在maya界面上的参考
# 特点：会自动保存在工作区上面，关掉maya不会清除窗口内容
# 开发时需要注意的点：在dock状态下不方便调试，开发时要在非dock状态以便调试
from PySide2 import QtWidgets
from shiboken2 import getCppPointer

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.OpenMayaUI import MQtUtil

import maya.cmds as cmds
# 多重继承中要把MayaQWidgetDockableMixin放在首位
class MyDockableButtonStatic(MayaQWidgetDockableMixin, QtWidgets.QPushButton):

    UI_NAME = "MyDockableButtonStatic" # 定义一个准确的UI_NAME使UI具有唯一性

    def __init__(self):
        super(MyDockableButtonStatic, self).__init__()

        self.setObjectName(self.UI_NAME)

        self.setWindowTitle("Dockable Window")
        self.setText("My Button")

        workspace_control_name = "{0}WorkspaceControl".format(self.UI_NAME)
        # 设置父级为工作区
        if cmds.workspaceControl(workspace_control_name, q=True, exists=True):
            workspace_control_ptr = long(MQtUtil.findControl(workspace_control_name))
            widget_ptr = long(getCppPointer(self)[0])

            MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)

if __name__ == "__main__":
    try:
        if button and button.parent():
            workspace_control_name = button.parent().objectName()

            if cmds.window(workspace_control_name, exists=True):
                cmds.deleteUI(workspace_control_name)
    except:
        pass

    button = MyDockableButtonStatic()

    ui_script = "from dockable_button_example import MyDockableButtonStatic\nbutton = MyDockableButtonStatic()"
    button.show(dockable=True, uiScript=ui_script) # 调用MayaQWidgetDockableMixin模块的show方法来使创建的窗口能够dock
