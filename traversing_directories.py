# coding:utf-8
# 以树状结构显示指定路径下的所有内容，并且可以通过右键打开资源管理器并进入路径
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class FileExplorerDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "File Explorer"

    DIRECTOR_PATH = "{0}scripts".format(cmds.internalVar(userAppDir=True))

    def __init__(self, parent=maya_main_window()):
        super(FileExplorerDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.tree_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) # 使Context菜单只针对tree_wdg
        self.tree_wdg.customContextMenuRequested.connect(self.show_context_menu) # 使Context菜单为自定义的并给出菜单

        self.refresh_list()

    def create_actions(self):
        self.show_in_folder_action = QtWidgets.QAction("Show in Folder", self)

    def create_widgets(self):
        self.path_label = QtWidgets.QLabel(self.DIRECTOR_PATH)

        self.tree_wdg = QtWidgets.QTreeWidget()
        self.tree_wdg.setHeaderHidden(True)

        self.close_btn = QtWidgets.QPushButton("Close")
    
    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2) # 设置左上右下的边距
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(self.tree_wdg)
        main_layout.addLayout(button_layout)
    
    def create_connections(self):
        self.close_btn.clicked.connect(self.close)
        self.show_in_folder_action.triggered.connect(self.show_in_folder)

    def refresh_list(self):
        """ 显示文件树状结构 """
        self.tree_wdg.clear()

        self.add_children(None, self.DIRECTOR_PATH)
    
    def add_children(self, parent_item, dir_path):
        """ 添加所有的子节点 """
        directory = QtCore.QDir(dir_path) # 创建目录为dir_path的QDir对象
        # entryList作用是得到目录下的所有文件的字符串列表，参数第一个是设置过滤器，这里是要所有项并且没有.和..   第二个是设置排列，目录在最上方并且不区分大小写
        files_in_directory = directory.entryList(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries, QtCore.QDir.DirsFirst | QtCore.QDir.IgnoreCase) 

        for file_name in files_in_directory:
            self.add_child(parent_item, dir_path, file_name)

    def add_child(self, parent_item, dir_path, file_name):
        """ 实现添加子节点 """
        file_path = "{0}/{1}".format(dir_path, file_name)
        file_info = QtCore.QFileInfo(file_path)

        if file_info.suffix().lower() == "pyc": # 过滤后缀为pyc的文件
            return

        item = QtWidgets.QTreeWidgetItem(parent_item, [file_name])
        item.setData(0, QtCore.Qt.UserRole, file_path) # QtCore.Qt.UserRole可以理解为序号0,一个item可以拥有多个数据，因此可以通过QtCore.Qt.UserRole，QtCore.Qt.UserRole+1来设置数据的序号

        if file_info.isDir():
            """ 如果是文件夹就用add_children方法 """
            self.add_children(item, file_info.absoluteFilePath())

        if not parent_item:
            """ 将item添加到最顶层树结构中 """
            self.tree_wdg.addTopLevelItem(item)

    def show_context_menu(self, pos):
        """ 自定义菜单 """
        item = self.tree_wdg.itemAt(pos) # 鼠标位置处的item
        if not item:
            return
        
        file_path = item.data(0, QtCore.Qt.UserRole) # 得到item里的数据
        self.show_in_folder_action.setData(file_path) # 设置action对应的数据

        context_menu = QtWidgets.QMenu() # 创建一个菜单
        context_menu.addAction(self.show_in_folder_action) # 将action添加到菜单下
        context_menu.exec_(self.tree_wdg.mapToGlobal(pos)) # 在鼠标位置处右键显示菜单

    def show_in_folder(self):
        file_path = self.show_in_folder_action.data()
        
        if cmds.about(windows=True): # 如果是windows系统就使用windows系统的方法打开资源管理器
            if self.open_in_explorer(file_path): 
                return
        elif cmds.about(macOS=True): # 如果是mac系统就使用mac系统的方法打开资源管理器
            if self.open_in_finder(file_path):
                return
        # 两个方法都不可以的情况下，使用Qt自带的方法打开，缺点是不能自动选择对应的文件
        file_info = QtCore.QFileInfo(file_path)
        if file_info.isDir(): # 如果是路径是目录就直接使用
            QtGui.QDesktopServices.openUrl(file_path)
        else: # 如果是文件就通过file_info.path方法得到目录路径
            QtGui.QDesktopServices.openUrl(file_info.path())
    
    def open_in_explorer(self, file_path):
        """ Windows打开资源管理器 """
        file_info = QtCore.QFileInfo(file_path)
        args = []
        if not file_info.isDir(): # 如果不是目录就选择路径对应的文件
            args.append("/select,")
        
        args.append(QtCore.QDir.toNativeSeparators(file_path))

        if QtCore.QProcess.startDetached("explorer", args):
            return True
        
        return False
    
    def open_in_finder(self, file_path):
        args = []
        args.append('-e')
        args.append('tell application "Finder"')
        args.append('-e')
        args.append('activate')
        args.append('-e')
        args.append('select POSIX file "{0}"'.format(file_path))
        args.append('-e')
        args.append('end tell')
        args.append('-e')
        args.append('return')

        if(QtCore.QPrecess.startDetached("/usr/bin/osascript", args)):
            return True
        
        return False
    
    
if __name__ == "__main__":

    try:
        my_dialog.close()  
        my_dialog.deleteLater()
    except:
        pass

    my_dialog = FileExplorerDialog()
    my_dialog.show()
    
        