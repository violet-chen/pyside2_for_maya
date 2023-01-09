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

class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):
    """ 输入文本编辑器 """
    def __init__(self, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)
    
    def keyPressEvent(self, key_event):
        """ 重载keyPressEvent方法 """
        # print("Key Pressed: {0}".format(key_event.text()))

        ctrl = key_event.modifiers() == QtCore.Qt.ControlModifier # ctrl为布尔值，代表ctrl键是否处于按下的状态
        # print("Control Modifiers: {0}".format(ctrl))

        shift = key_event.modifiers() == QtCore.Qt.ShiftModifier
        # print("Shift Modifiers: {0}".format(shift))

        alt = key_event.modifiers() == QtCore.Qt.AltModifier
        # print("Alt Modifiers: {0}".format(alt))

        ctrl_alt = key_event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
        # print("Ctrl+Alt Modifiers: {0}".format(ctrl_alt))

        # if shift:
        #     return

        key = key_event.key()

        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            """ Key_Return代表中间的回车键 Key_Enter代表右边的回车键 """
            if ctrl: # 如果是ctrl+enter
                print("Execute Code")
            elif ctrl_alt: # 如果是ctrl+alt+enter
                print("Execute Line")
                return
        
        super(CustomPlainTextEdit, self).keyPressEvent(key_event) # 重载QtWidgets.QPlainTextEdit的keyPressEvent方法的同时，不影响keyPressEvent的功能

class KeyPressExample(QtWidgets.QDialog):

    WINDOW_TITLE = "Keypress Example"

    def __init__(self, parent=maya_main_window()):
        super(KeyPressExample, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(300, 80)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """ 控件 """
        self.plain_text = CustomPlainTextEdit()

    def create_layouts(self):
        """ 布局 """
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addWidget(self.plain_text)



if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    
    ui = KeyPressExample()
    ui.show()
