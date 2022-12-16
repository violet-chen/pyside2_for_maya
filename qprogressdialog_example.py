# coding:utf-8
import time
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds



def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ProgressTestDialog(QtWidgets.QDialog):
    WINDOW_TITLE = "Progress Test"

    def __init__(self, parent=maya_main_window()):
        super(ProgressTestDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(300, 120)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.progress_bar_button = QtWidgets.QPushButton("Do It!")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.progress_bar_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.progress_bar_button.clicked.connect(self.run_progress_test)

    def run_progress_test(self):
        number_of_operations = 10  # 循环的数量

        progress_dialog = QtWidgets.QProgressDialog("Waiting to process...", "Cancel", 0, number_of_operations, self)
        progress_dialog.setWindowTitle("Progress...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)  # 设置为进度条窗口出现时，代码依然能够执行，但是不能使用除对话框之外的操作
        progress_dialog.show()

        QtCore.QCoreApplication.processEvents()  # 在执行代码之前显示对话框

        for i in range(1, number_of_operations + 1):
            if progress_dialog.wasCanceled():  # 当按了cancel按钮后中止代码
                break
            progress_dialog.setLabelText("Processing operation: {0} (fo {1})".format(i, number_of_operations))
            progress_dialog.setValue(i)
            time.sleep(0.5)

            QtCore.QCoreApplication.processEvents()  # 显示对话框的内容

        progress_dialog.close()



if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = ProgressTestDialog()
    ui.show()