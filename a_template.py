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


class TestDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "MAYA-2018"
    UI_NAME = "TemplateUI"

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(300, 80)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setObjectName(self.UI_NAME)
        styleSheet = '''
        QWidget {
            font: 70 14pt "Bradley Hand ITC";
            color: rgb(200,200,200);

        }
        QPushButton{
            border-style: outset;
            border-width: 2px;
            border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-bottom-color: rgb(58, 58, 58);
            border-bottom-width: 1px;
            border-style: solid;
            color: rgb(255, 255, 255);
            padding: 2px;
            background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
        }

        QPushButton:hover{
            border-style: outset;
            border-width: 2px;
            border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
            border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
            border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
            border-bottom-color: rgb(115, 115, 115);
            border-bottom-width: 1px;
            border-style: solid;
            color: rgb(255, 255, 255);
            padding: 2px;
            background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(157, 157, 157, 255));
        }

        QPushButton:pressed{
            border-style: outset;
            border-width: 2px;
            border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(62, 62, 62, 255), stop:1 rgba(22, 22, 22, 255));
            border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-bottom-color: rgb(58, 58, 58);
            border-bottom-width: 1px;
            border-style: solid;
            color: rgb(255, 255, 255);
            padding: 2px;
            background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
        }

        QPushButton:disabled{
            border-style: outset;
            border-width: 2px;
            border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
            border-bottom-color: rgb(58, 58, 58);
            border-bottom-width: 1px;
            border-style: solid;
            color: rgb(0, 0, 0);
            padding: 2px;
            background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(57, 57, 57, 255), stop:1 rgba(77, 77, 77, 255));
        }
        QListWidget{
            border-radius:4px;
            border: 1px solid rgba(222,222,222,50%);
            background: rgba(100,100,100,100%);
            color: rgb(255,255,255);
        }
        QListWidget::Item:selected{
            background-color: rgb(80, 80, 80);
            border-left: 5px solid rgb(150, 150, 150);
            border-right: 1px solid rgb(150, 150, 150);
            border-top: 1px solid rgb(150, 150, 150);
            border-bottom: 1px solid rgb(150, 150, 150);
            color: rgb(255,255,255);
        }
        QLineEdit{
            border-radius:4px;
            background: rgba(100,100,100,40%);
            border: 1px solid rgba(222,222,222,50%);
            color: rgb(255,255,255);
        }
        QLabel{
            background: transparent;
        }
        QComboBox{
            border: 1px solid rgba(222,222,222,50%);
            border-radius:4px;
            background-color: rgb(80, 80, 80);
            selection-background-color: rgb(80,80,80);
            color: rgb(90, 90, 90);
        }
        QComboBox QAbstractItemView{
            background-color: rgb(80, 80, 80);
            selection-background-color: rgb(150,150,150);
            }
        }
        #TemplateUI{
            background-color: qlineargradient(spread:pad, x1:1, y1:0.023, x2:1, y2:1, stop:0 rgba(43, 41, 41, 255), stop:1 rgba(116, 116, 116, 255));        }
        '''
        self.setStyleSheet(styleSheet)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """ 控件 """
        pass

    def create_layouts(self):
        """ 布局 """
        pass

    def create_connections(self):
        """ 信号与槽的连接 """
        pass



if __name__ == '__main__':
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = TestDialog()
    ui.show()
