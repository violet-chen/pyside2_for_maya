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

class LightItem(QtWidgets.QWidget):

    SUPPORTED_TYPES = ["ambientLight", "directionalLight", "pointLight", "spotLight"]
    EMIT_TYPES = ["directionalLight", "pointLight", "spotLight"]

    def __init__(self, shape_name, parent=None):
        super(LightItem, self).__init__(parent)

        self.setFixedHeight(26)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        self.light_type_btn = QtWidgets.QPushButton()
        self.light_type_btn.setFixedSize(20, 20)

        self.visiblity_cb = QtWidgets.QCheckBox()
        
        self.transform_name_label = QtWidgets.QLabel("placeholder")
        self.transform_name_label.setFixedWidth(120)
        self.transform_name_label.setAlignment(QtCore.Qt.AlignCenter)
    
    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.light_type_btn)
        main_layout.addWidget(self.visiblity_cb)
        main_layout.addWidget(self.transform_name_label)

        main_layout.addStretch()
    
    def create_connections(self):
        pass

class LightPanel(QtWidgets.QDialog):

    WINDOW_TITLE = "Light Panel"

    def __init__(self, parent=maya_main_window()):
        super(LightPanel, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(500, 260)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        window_name = "WindowName"
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)
        self.setObjectName(window_name)

        self.light_items = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """ 控件 """
        self.refreshButton = QtWidgets.QPushButton("Refresh Lights")

    def create_layouts(self):
        """ 布局 """
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Light"))
        header_layout.addSpacing(50)
        header_layout.addWidget(QtWidgets.QLabel("Intensity"))
        header_layout.addSpacing(44)
        header_layout.addWidget(QtWidgets.QLabel("Color"))
        header_layout.addSpacing(24)
        header_layout.addWidget(QtWidgets.QLabel("Emit Diffuse"))
        header_layout.addSpacing(10)
        header_layout.addWidget(QtWidgets.QLabel("Emit Spec"))
        header_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refreshButton)

        light_list_wdg = QtWidgets.QWidget()

        self.light_layout = QtWidgets.QVBoxLayout(light_list_wdg) # light_list_wdg在light_layout下
        self.light_layout.setContentsMargins(2, 2, 2, 2)
        self.light_layout.addSpacing(3)
        self.light_layout.setAlignment(QtCore.Qt.AlignTop)

        light_list_scroll_area = QtWidgets.QScrollArea()
        light_list_scroll_area.setWidgetResizable(True)
        light_list_scroll_area.setWidget(light_list_wdg) # scroll_area下有light_list_wdg

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(light_list_scroll_area) # 主布局下有个scroll_area
        main_layout.addLayout(button_layout)

    def create_connections(self):
        """ 信号与槽的连接 """
        self.refreshButton.clicked.connect(self.refresh_lights)
        
    def get_lights_in_scene(self):
        return cmds.ls(typ="light")

    def refresh_lights(self):
        self.clear_lights()

        scene_lights = self.get_lights_in_scene()
        for light in scene_lights:
            light_item = LightItem(light)

            self.light_layout.addWidget(light_item)
            self.light_items.append(light_item)
            
    
    def clear_lights(self):
        self.light_items = []
        
        while self.light_layout.count() > 0:
            light_item = self.light_layout.takeAt(0)
            if light_item.widget():
                light_item.widget().deleteLater()

    def showEvent(self, event):
        """ 当打开窗口时执行 """
        self.refresh_lights()
    
    def closeEvent(self, event):
        """ 当关闭窗口时执行 """
        self.clear_lights()

if __name__ == '__main__':
    try:
        light_panel_dialog.close()
        light_panel_dialog.deleteLater()
    except:
        pass
    light_panel_dialog = LightPanel()
    light_panel_dialog.show()
