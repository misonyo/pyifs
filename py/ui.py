# -*- coding:utf-8 -*-
import sys
import os
import pyifs
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(1)
        self.setHeaderLabels([''])

        self.clicked.connect(self.ClickEvent)
        
    def AddTopItem(self,text):
        topLevelItem = QTreeWidgetItem()
        self.addTopLevelItem(topLevelItem)
        topLevelItem.setText(0,text)
    
    def AddSubItem(self,TopItem,text):
        subItem=QTreeWidgetItem(TopItem)
        subItem.setText(0,text)
        
    def ClickEvent(self):
        item=self.currentItem()
        print(item.text(0))
        #pyifs = pyifs(ifs)

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Name','Size','Type','Modified'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.clicked.connect(self.ClickEvent)

    def AddItem(self,label):
        name = QTableWidgetItem(label[0])
        self.setItem(0,0,name)
        
        size = QTableWidgetItem(label[1])
        self.setItem(0,0,size)
        
        type = QTableWidgetItem(label[2])
        self.setItem(0,0,type)
        
        modified = QTableWidgetItem(label[3])
        self.setItem(0,0,modified)

    def ClickEvent(self):
        item=self.currentItem()

        
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def OpenAction(self):
        path = QFileDialog.getOpenFileName(self,"Open File Dialog",'',"image files(*.bin)")
        print(path)
        self.tree.AddTopItem(os.path.basename(path[0]))
        #self.tree.ClickEvent(path[0]))

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
 
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open image')
        openAction.triggered.connect(self.OpenAction)
 
        self.statusBar()
 
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)
        
        self.table = TableWidget()
        self.tree = TreeWidget()
        
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.table)

        self.setCentralWidget(splitter)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('pyifs')
        self.show()

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    