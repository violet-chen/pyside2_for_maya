# 让UI成为workspaceControl的widget，这样就能够创建出可以dock的UI了
from PySide2 import  QtCore
from PySide2 import  QtWidgets
from shiboken2 import getCppPointer

import maya.OpenMayaUI as omui
import maya.cmds as cmds


class WorkspaceControl(object):
    """ 根据workspaceControl命令自定义的方便使用类 """
    
    def __init__(self,name):
        self.name = name
        self.widget = None
    
    def create(self, label, widget, ui_script=None):
        
        cmds.workspaceControl(self.name, label=label)

        if ui_script:
            cmds.workspaceControl(self.name, e=True, uiScript=ui_script)
        
        self.add_widget_to_layout(widget)
        self.set_visible(True)

    def restore(self, widget):
        """ 恢复widget的显示 """
        self.add_widget_to_layout(widget)
    
    def add_widget_to_layout(self, widget):
        """ 将widget添加到layout上 """
        if widget:
            self.widget = widget
            self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors) # 参考mayaMixin推荐的一个属性设置，意思是我们的widget会跟随父窗口属性改变，但是不要跟随父窗口属性改变的同时将祖先窗口改变。

            workspace_control_ptr = long(omui.MQtUtil.findControl(self.name)) # 得到workspaceControl的指针
            widget_ptr = long(getCppPointer(self.widget)[0]) # 得到widget的cpp指针

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr) # 令我们的widget属于maya布局

    def exists(self):
        """ 判断workspaceControl是否存在 """
        return cmds.workspaceControl(self.name, q=True, exists=True)
    
    def is_visible(self):
        """ 判断workspaceControl可视性 """
        return cmds.workspaceControl(self.name, q=True, visible=True)
    
    def set_visible(self, visible):
        """ 设置workspaceControl的可视性 """
        if visible:
            cmds.workspaceControl(self.name, e=True, restore=True)
        else:
            cmds.workspaceControl(self.name, e=True, visible=False)
    
    def set_label(self, label):
        """ 设置workspaceControl的标签 """
        cmds.workspaceControl(self.name, e=True, label=label)
    
    def is_floating(self):
        """ 判断workspaceControl是否浮动 """
        return cmds.workspaceControl(self.name, q=True, floating=True)

    def is_collapsed(self):
        """ 判断workspaceControl是否收缩 """
        return cmds.workspaceControl(self.name, q=True, collapse=True)
    

class SampleUI(QtWidgets.QWidget):

    WINDOW_TITLE = "Sample UI"
    UI_NAME = "SampleUI"

    ui_instance = None

    # 创建一个类方法，方便外界调用来显示可以dock的UI,如果SampleUI存在就显示它，不存在就创建
    @classmethod
    def display(cls):
        if cls.ui_instance:
            cls.ui_instance.show_workspace_control()
        else:
            cls.ui_instance = SampleUI()

    @classmethod
    def get_workspace_control_name(cls):
        """ 设置控件对应的workspaceControl名字 """
        return "{0}WorkspaceControl".format(cls.UI_NAME)
    

    def __init__(self):
        super(SampleUI, self).__init__()

        self.setObjectName(self.__class__.UI_NAME)
        self.setMinimumSize(200, 100)

        self.create_widget()
        self.create_layout()
        self.create_connections()
        self.create_workspace_control()
    
    def create_widget(self):
        self.apply_button = QtWidgets.QPushButton("Apply")
    
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        main_layout.addWidget(self.apply_button)
    
    def create_connections(self):
        self.apply_button.clicked.connect(self.on_clicked)
    
    def create_workspace_control(self):
        """ 创建workspaceControl """
        self.workspace_control_instance = WorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self) # 如果workspace_control已经存在了那么就将它显示出来
        else:
            self.workspace_control_instance.create(self.WINDOW_TITLE, self, ui_script="from workspace_control import SampleUI\nSampleUI.display()")
    
    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)
    
    def on_clicked(self):
        print("Button Clicked")

    def showEvent(self, e):
        """ 设置窗口float时以及dock时对应的标题 """
        if self.workspace_control_instance.is_floating():
            self.workspace_control_instance.set_label("Floating Window")
        else:
            self.workspace_control_instance.set_label("Docked Window")



if __name__ == "__main__":

    workspace_control_name = SampleUI.get_workspace_control_name()
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)

    # 这串代码可以使UI在dock的同时能够通过更改UI的代码来更新界面
    # try:
    #     sample_ui.setParent(None)
    #     sample_ui.deleteLater()
    # except:
    #     pass
    
    sample_ui = SampleUI()
    sample_ui.show()