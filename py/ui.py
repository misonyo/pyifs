# -*- coding:utf-8 -*-
import sys
import os
import pyifs
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class TreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
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
        dir = self.parent.drive.path
        entry = self.parent.drive.ls(dir)
        print(">>>>>entry:",entry)
        ls = ["00","11","22","33"]
        self.parent.table.AddItems(ls)

class TableWidget(QTableWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent;
        
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Name','Size','Type','Modified'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.clicked.connect(self.ClickEvent)

    def AddItems(self,label):
        write_row = self.rowCount()
        self.setRowCount(self.rowCount()+1)
        name = QTableWidgetItem(label[0])
        self.setItem(write_row,0,name)
        
        size = QTableWidgetItem(label[1])
        self.setItem(write_row,1,size)
        
        type = QTableWidgetItem(label[2])
        self.setItem(write_row,2,type)
        
        modified = QTableWidgetItem(label[3])
        self.setItem(write_row,3,modified)

    def ClickEvent(self):
        item=self.currentItem()

        
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def OpenAction(self):
        path = QFileDialog.getOpenFileName(self,"Open File Dialog",'',"image files(*.bin)")
        print(">>>>>>path",path)
        self.tree.AddTopItem(os.path.basename(path[0]))
        print(">>>>>>path[0]",path[0])
        self.drive = pyifs.pyifs(os.path.basename(path[0]))

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
        
        self.table = TableWidget(self)
        self.tree = TreeWidget(self)
        
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
    