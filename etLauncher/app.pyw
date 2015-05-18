#!/usr/bin/python

import os
import sys
from PySide import QtCore
from PySide import QtGui

from etLauncher.launcher import Launcher


class LauncherUI(QtGui.QMainWindow):

    def __init__(self):
        super(LauncherUI, self).__init__()
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self._resourceDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

        self._styleSheet = """

        QMainWindow {
            color: white;
            margin: 0;
            padding: ;
            border: 1px solid #151515;
            background-color: #222222;
        }

        QMainWindow::QToolBar {
            background-color: yellow;
        }

        QMenuBar {
            padding: 5px 0px;
            color: white;
            width: 75px;
            background-color: #151515;
            text-align: center;
            text-transform: lowercase;
            font-size: 12pt;
            font-weight: bold;
            border-right: 1px solid black;
        }

        QMenuBar::item {
            color: white;
            padding: 3px 0px;
            font-weight: bold;
            border-right: 1px solid #222;
        }

        QMenuBar::item:selected {
            color: #4079ff;
            font-weight: bold;
        }

        QFrame#logoFrame {
            padding: 0px;
            margin: 0px;
            background-image: url(resources/logo.png);
        }

        QListWidget {
            margin: 0px;
            padding: 0px;
            border-top: 1px solid #111;
            border-right: 1px solid #252525;
            border-bottom: 1px solid #252525;
            border-left: 1px solid #111;
            color: white;
            background-color: #111;
            alternate-background-color: yellow;
        }

        QListWidget::item {
            border: 0px;
            height: 35px;
            color: white;
        }

        QListWidget::item:alternate {
            background-color: #252525;
        }

        QListWidget::item:selected {
            background-color: #222;
        }

        QListWidget::item:hover {
            background-color: #353535;
        }

        QStatusBar {
            color: #898989;
            background-color: #333333;
        }

        QPushButton {
            color: white;
            padding: 5px;
            border-width: 2px;
            border-radius: 5px;
            background-color: #333;
        }

        QPushButton:hover {
            color: #4079ff;
            border-width: 2px;
            border-color: black;
            background-color: #313131;
        }

        QPushButton#launchButton {
            font-size: 12pt;
            font-weight: bold;
            text-transform: lowercase;
        }

        """

        self.setStyleSheet(self._styleSheet)

        self._launcher = Launcher()

        self.initUI()


    def mousePressEvent(self, event):
        self.offset = event.pos()


    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


    def getLauncher(self):

        return self._launcher


    def launchPreset(self):

        launcher = self.getLauncher()
        currentSel = self.presetList.currentItem()
        # launcher.launch(currentSel.text())

        self.statusBar().showMessage('Launching: ' + currentSel.text())


    def setupMainLayout(self):

        # Main Layout
        self.mainLayoutWidget = QtGui.QWidget()
        self.mainLayoutWidget.setContentsMargins(0, 0, 0, 0)

        # ===============
        # Layout Widgets
        # ===============

        # Outer VBox Layout
        self.outerVBox = QtGui.QVBoxLayout(self.mainLayoutWidget)
        self.outerVBox.setObjectName('outerVBox')
        self.outerVBox.setContentsMargins(0, 0, 0, 0)
        self.outerVBox.setSpacing(0)
        self.outerVBox.layout().setContentsMargins(0, 0, 0, 0)

        # Main Content HBox Layout
        self.mainContentHBox = QtGui.QHBoxLayout()
        self.mainContentHBox.setObjectName('mainContentHBox')
        self.mainContentHBox.setContentsMargins(0, 0, 0, 0)
        self.mainContentHBox.setSpacing(0)
        self.mainContentHBox.layout().setContentsMargins(0, 0, 0, 0)

        # Bottom Content HBox Layout
        self.bottomContentHBox = QtGui.QHBoxLayout()
        self.bottomContentHBox.setObjectName('bottomContentHBox')
        self.bottomContentHBox.setContentsMargins(0, 0, 0, 0)
        self.bottomContentHBox.setSpacing(0)
        self.bottomContentHBox.layout().setContentsMargins(0, 0, 0, 0)

        # ========
        # Widgets
        # ========
        # Logo
        self.logo = QtGui.QFrame(self)
        self.logo.setObjectName('logoFrame')
        self.logo.setContentsMargins(0, 0, 0, 0)
        self.logo.setMinimumWidth(500)
        self.logo.setMinimumHeight(50)
        self.logo.setMaximumHeight(50)

        # Menu Bar
        self.myMenuBar = QtGui.QMenuBar()
        self.myMenuBar.setContentsMargins(0, 0, 0, 0)
        self.myMenuBar.setObjectName('mainMenu')

        # File Menu
        self.fileMenu = self.myMenuBar.addMenu('&File')
        self.fileMenu.addAction('&Import')
        self.fileMenu.addAction('&Export')
        # self.fileMenu.addAction(exitAction)

        # Edit Menu
        self.editMenu = self.myMenuBar.addMenu('&Edit')
        self.editMenu.addAction('&Apps')
        self.editMenu.addAction('&Environments')
        self.editMenu.addAction('&Presets')

        self.myMenuBar.addSeparator()

        # Close Menu
        exitAction = QtGui.QAction('&Close', self)
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Close application')
        exitAction.triggered.connect(self.close)
        self.myMenuBar.addAction(exitAction)

        # ============
        # Preset List
        # ============
        self.presetList = QtGui.QListWidget(self)
        self.presetList.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.presetList.setMinimumWidth(500)
        # self.presetList.setAlternatingRowColors(True)

        launcher = self.getLauncher()
        presets = launcher.getProcessor().getPresets()
        for preset in presets.keys():
            QtGui.QListWidgetItem(preset, self.presetList)

        self.presetList.setCurrentItem(self.presetList.item(0))

        # ===============
        # Bottom Content
        # ===============
        # Launch Button
        self.launchButton = QtGui.QPushButton('Launch', self)
        self.launchButton.setObjectName('launchButton')
        self.launchButton.setMinimumHeight(40)
        self.launchButton.setMinimumWidth(500)
        self.launchButton.setMaximumWidth(500)
        self.launchButton.clicked.connect(self.launchPreset)
        self.launchButton.setToolTip('Launch Preset!')

        # =======================
        # Add Widgets to Layouts
        # =======================
        self.outerVBox.addWidget(self.logo)
        self.outerVBox.addWidget(self.myMenuBar)
        self.outerVBox.addSpacing(20)
        self.outerVBox.addLayout(self.mainContentHBox)
        self.outerVBox.addSpacing(20)
        self.outerVBox.addLayout(self.bottomContentHBox)
        self.outerVBox.addStretch(1)

        # Main Content
        self.mainContentHBox.addStretch(1)
        self.mainContentHBox.addWidget(self.presetList)
        self.mainContentHBox.addStretch(1)

        # Bottom Content
        self.bottomContentHBox.addStretch(1)
        self.bottomContentHBox.addWidget(self.launchButton)
        self.bottomContentHBox.addStretch(1)


    def initUI(self):

        self.statusBar().showMessage('Ready')

        self.setupMainLayout()
        self.setCentralWidget(self.mainLayoutWidget)

        # Setup Geo and Window
        self.setGeometry(250, 150, 600, 400)
        self.setWindowTitle('ET Launcher')
        self.center()

        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():

    app = QtGui.QApplication(sys.argv)
    ex = LauncherUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()