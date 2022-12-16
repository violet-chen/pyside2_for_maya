# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):
    FILE_FILTERS = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项

    selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle('Open/Import/Reference')
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.create_title_label()

        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton()
        self.select_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.select_file_path_btn.setToolTip("select File")

        self.open_rb = QtWidgets.QRadioButton("Open")
        self.open_rb.setChecked(True)
        self.import_rb = QtWidgets.QRadioButton("Import")
        self.reference_rb = QtWidgets.QRadioButton("Reference")

        self.force_cb = QtWidgets.QCheckBox("Force")

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_title_label(self):
        image_path = "D:/ZhangRuiChen/image/test_image.jpg"
        image = QtGui.QImage(image_path)
        image = image.scaled(280, 100, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image)

        self.title_label = QtWidgets.QLabel("My Awesome Utility")
        self.title_label.setPixmap(pixmap)

    def create_layouts(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_file_path_btn)

        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.open_rb)
        radio_btn_layout.addWidget(self.import_rb)
        radio_btn_layout.addWidget(self.reference_rb)

        forme_layout = QtWidgets.QFormLayout()
        forme_layout.addRow("File", file_path_layout)
        forme_layout.addRow("", radio_btn_layout)
        forme_layout.addRow("", self.force_cb)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(forme_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)

        self.open_rb.toggled.connect(self.update_force_visibility)

        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)

    def show_file_select_dialog(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "",
                                                                                self.FILE_FILTERS, self.selected_filter)
        if file_path:
            self.filepath_le.setText(file_path)

    def update_force_visibility(self, checked):
        self.force_cb.setVisible(checked)

    def load_file(self):
        file_path = self.filepath_le.text()
        if not file_path:
            return

        file_info = QtCore.QFileInfo(file_path)  # 得到文件的信息
        if not file_info.exists():  # 判断文件是否存在
            om.MGlobal.displayError("File does not exist: {}".format(file_path))
            return
        if self.open_rb.isChecked():
            self.open_file(file_path)
        if self.import_rb.isChecked():
            self.import_file(file_path)
        else:
            self.reference_file(file_path)

    def open_file(self, file_path):
        force = self.force_cb.isChecked()
        if not force and cmds.file(q=True, modified=True):
            result = QtWidgets.QMessageBox.question(self, "Modified", "Current scene has unsaved changes. Continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                force = True
            else:
                return
        cmds.file(file_path, open=True, ignoreVersion=True, force=force)

    def import_file(self, file_path):
        cmds.file(file_path, i=True, ignoreVersion=True)

    def reference_file(self, file_path):
        cmds.file(file_path, r=True, ignoreVersion=True)


if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
