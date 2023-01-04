# coding:utf-8
# 灯光面板举例
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

class LightItem(QtWidgets.QWidget):

    SUPPORTED_TYPES = ["ambientLight", "directionalLight", "pointLight", "spotLight", "areaLight"]
    EMIT_TYPES = ["directionalLight", "pointLight", "spotLight", "areaLight"]

    def __init__(self, shape_name, parent=None):
        super(LightItem, self).__init__(parent)

        self.setFixedHeight(26)

        self.shape_name = shape_name

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        self.light_type_btn = QtWidgets.QPushButton()
        self.light_type_btn.setFixedSize(20, 20)
        self.light_type_btn.setFlat(True) # 设置按钮的显示形式

        self.visiblity_cb = QtWidgets.QCheckBox()
        
        self.transform_name_label = QtWidgets.QLabel("placeholder")
        self.transform_name_label.setFixedWidth(120)
        self.transform_name_label.setAlignment(QtCore.Qt.AlignCenter)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb = QtWidgets.QDoubleSpinBox()
            self.intensity_dsb.setRange(0.0, 100.0)
            self.intensity_dsb.setDecimals(3) # 设置数值到小数点后三位
            self.intensity_dsb.setSingleStep(0.1)
            self.intensity_dsb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons) # 设置spinbox没有上下箭头

            self.color_btn = CustomColorButton()

            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb = QtWidgets.QCheckBox()
                self.emit_specular_cb = QtWidgets.QCheckBox()
        
        self.update_values()
    
    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.light_type_btn)
        main_layout.addWidget(self.visiblity_cb)
        main_layout.addWidget(self.transform_name_label)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            main_layout.addWidget(self.intensity_dsb)
            main_layout.addSpacing(10)
            main_layout.addWidget(self.color_btn)

            if light_type in self.EMIT_TYPES:
                main_layout.addSpacing(34)
                main_layout.addWidget(self.emit_diffuse_cb)
                main_layout.addSpacing(50)
                main_layout.addWidget(self.emit_specular_cb)

        main_layout.addStretch()
    
    def create_connections(self):
        self.light_type_btn.clicked.connect(self.select_light)
        self.visiblity_cb.toggled.connect(self.set_visibility)
        
        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.editingFinished.connect(self.on_intensity_changed)
            self.color_btn.color_changed.connect(self.set_color)

            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.toggled.connect(self.set_emit_diffuse)
                self.emit_specular_cb.toggled.connect(self.set_emit_specular)

    def update_values(self):
        self.light_type_btn.setIcon(self.get_light_type_icon())
        self.visiblity_cb.setChecked(self.is_visible())
        self.transform_name_label.setText(self.get_transform_name())

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.setValue(self.get_intensity())
            self.color_btn.set_color(self.get_color())
            
            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.setChecked(self.emits_diffuse())
                self.emit_specular_cb.setChecked(self.emits_specular())

    def get_transform_name(self):
        return cmds.listRelatives(self.shape_name, parent=True)[0]

    def get_attribute_value(self, name, attribute):
        return cmds.getAttr("{0}.{1}".format(name, attribute))

    def set_attribute_value(self, name, attribute,*args):
        attr_name = "{0}.{1}".format(name, attribute)
        cmds.setAttr(attr_name, *args)

    def get_light_type(self):
        return cmds.objectType(self.shape_name)

    def get_light_type_icon(self):
        light_type = self.get_light_type()

        icon = QtGui.QIcon()
        if light_type == "ambientLight":
            icon = QtGui.QIcon(":ambientLight.svg")
        elif light_type == "directionalLight":
            icon = QtGui.QIcon(":directionalLight.svg")
        elif light_type == "pointLight":
            icon = QtGui.QIcon(":pointLight.svg")
        elif light_type == "spotLight":
            icon = QtGui.QIcon(":spotLight.svg")
        else:
            icon = QtGui.QIcon(":Light.png")

        return icon

    def is_visible(self):
        transform_name = self.get_transform_name()
        return self.get_attribute_value(transform_name, "visibility")
    
    def get_intensity(self):
        return self.get_attribute_value(self.shape_name, "intensity")

    def get_color(self):
        temp_color = self.get_attribute_value(self.shape_name, "color")[0]
        return QtGui.QColor(temp_color[0] * 255, temp_color[1] * 255, temp_color[2] * 255)

    def emits_diffuse(self):
        return self.get_attribute_value(self.shape_name, "emitDiffuse")

    def emits_specular(self):
        return self.get_attribute_value(self.shape_name, "emitSpecular")
    
    def select_light(self):
        cmds.select(self.get_transform_name)

    def set_visibility(self, checked):
        self.set_attribute_value(self.get_transform_name(), "visibility", checked)
    
    def on_intensity_changed(self):
        self.set_attribute_value(self.shape_name, "intensity", self.intensity_dsb.value())
    
    def set_color(self, color):
        self.set_attribute_value(self.shape_name, "color", color.redF(), color.greenF(), color.blueF())
    
    def set_emit_diffuse(self, checked):
        self.set_attribute_value(self.shape_name, "emitDiffuse", checked)

    def set_emit_specular(self, checked):
        self.set_attribute_value(self.shape_name, "emitSpecular", checked)
    

class LightPanel(QtWidgets.QDialog):

    WINDOW_TITLE = "Light Panel"

    def __init__(self, parent=maya_main_window()):
        super(LightPanel, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(500, 260)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.light_items = []
        self.script_jobs = []

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
    
    def create_script_jobs(self):
        self.script_jobs.append(cmds.scriptJob(event=["DagObjectCreated", partial(self.on_dag_object_created)])) # 当创建dag物体时执行on_dag_object_created函数
        self.script_jobs.append(cmds.scriptJob(event=["Undo", partial(self.on_undo)])) # 当ctrl+z时执行on_undo函数

    def delete_script_jobs(self):
        for job_number in self.script_jobs:
            cmds.scriptJob(kill=job_number)

        self.script_jobs = []

    def on_dag_object_created(self):
        if len(cmds.ls(typ="light")) != len(self.light_items):
            print("New light created...")
            self.refresh_lights()

    def on_undo(self):
        if len(cmds.ls(typ="light")) != len(self.light_items):
            print("Undo light created...")
            self.refresh_lights()

    def showEvent(self, event):
        """ 当打开窗口时执行 """
        self.refresh_lights()
        self.create_script_jobs()
    
    def closeEvent(self, event):
        """ 当关闭窗口时执行 """
        self.clear_lights()
        self.delete_script_jobs()

if __name__ == '__main__':
    cmds.file(new=True,f=True)
    cmds.file("D:/ZhangRuiChen/Pyside2ForMaya/light_test.ma",o=True,f=True)
    try:
        light_panel_dialog.close()
        light_panel_dialog.deleteLater()
    except:
        pass
    light_panel_dialog = LightPanel()
    light_panel_dialog.show()
