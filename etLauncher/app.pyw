#!/usr/bin/python

import sys
from PySide import QtGui

from etLauncher.launcher import Launcher


class LauncherUI(QtGui.QMainWindow):

    def __init__(self):
        super(LauncherUI, self).__init__()
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)

        self._launcher = Launcher()

        self.initUI()


    def getLauncher(self):

        return self._launcher


    def launchPreset(self):

        launcher = self.getLauncher()
        currentSel = self.presetList.currentItem()
        # launcher.launch(currentSel.text())

        self.statusBar().showMessage('Launching: ' + currentSel.text())


    def setupMainLayout(self):

        self.mainLayoutWidget = QtGui.QWidget()

        # Layout
        self.vbox = QtGui.QVBoxLayout(self.mainLayoutWidget)

        # Widgets
        self.presetList = QtGui.QListWidget(self)
        self.presetList.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        launcher = self.getLauncher()
        presets = launcher.getProcessor().getPresets()

        for preset in presets.keys():
            QtGui.QListWidgetItem(preset, self.presetList)

        self.presetList.setCurrentItem(self.presetList.item(0))

        self.btn = QtGui.QPushButton('Launch', self)
        self.btn.setMinimumHeight(40)
        self.btn.clicked.connect(self.launchPreset)
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.btn.resize(self.btn.sizeHint())

        # Add Widgets
        self.vbox.addWidget(self.presetList)
        self.vbox.addWidget(self.btn)

        # self.vbox.addStretch(1)


    def initUI(self):

        # Actions
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

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