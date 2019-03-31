import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QPushButton, QDesktopWidget,
                            QLabel, QFileDialog, QWidget, QGridLayout, QMenu, QSizePolicy, QMessageBox, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from win32api import GetSystemMetrics

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

import random

CURRENT_VERSION = 0.1

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('test')

        window_width = GetSystemMetrics(0)
        window_height = GetSystemMetrics(1)

        self.resize(0.6 * window_width, 0.6 * window_height)
        self.center()

        self.setWindowIcon(QIcon('Icon.png'))

        #inits
        self.openDirectoryDialog = ""
        self.data = np.empty(shape=(1,2), dtype=np.float)

        #Exit on menubar
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit applicatiion')
        exitAct.triggered.connect(qApp.quit)

        #Open on menubar
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open Directory')
        openAct.triggered.connect(self.openFile)

        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openAct)

        #Central
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)

        #Grid
        grid = QGridLayout(centralwidget)
        self.setLayout(grid)

        #Plot
        plotCan = PlotCanvas(self, width=5, height=4)
        grid.addWidget(plotCan , 0,1)

        #button
        btn = QPushButton("Load Data", centralwidget)
        btn.resize(btn.sizeHint())
        grid.addWidget(btn, 0,0)

        btn.clicked.connect(lambda:plotCan .plot(self.data))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile(self):
        self.csvFile = QFileDialog.getOpenFileName(self, "Get Dir Path")[0]
        self.data = np.loadtxt(self.csvFile, delimiter=',', dtype='S')[2:].astype(np.float)

    def buttonpress(self):
        self.plot(self.data)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data = np.empty(shape=(1,2))):
        ax = self.figure.add_subplot(111)
        ax.plot(data[:,0],data[:,1], 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())