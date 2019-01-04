# -*- coding:utf-8 -*-
import sys
import os
import pyifs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
#from bitarray._bitarray import length

class TopItem(QTreeWidgetItem):
    def __init__(self,path):
        super().__init__()
        self.WinPath = path
        self.drive = pyifs.pyifs(path)
        self.setText(0,os.path.basename(path))
        self.setText(1,"TopItem")
        self.setIcon(0,QIcon('../figures/dir.png'))
    
class ChildItem(QTreeWidgetItem):
    def __init__(self,text):
        super().__init__()
        self.setText(0,text)
        self.setText(1,"ChildItem")
        self.setIcon(0,QIcon('../figures/dir.png'))
        self.setExpanded(True)
        
class TreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setColumnCount(1)
        self.setHeaderLabels([''])

class TableWidget(QTableWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent;
        
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Name','Size','Type','Modified'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def AddItems(self,label):
        write_row = self.rowCount()
        self.setRowCount(self.rowCount()+1)
        name = QTableWidgetItem(label[0])
        self.setItem(write_row,0,name)
        
        size = QTableWidgetItem(label[1])
        self.setItem(write_row,1,size)
        
        type = QTableWidgetItem(label[2])
        self.setItem(write_row,2,type)
        
        if (label[2] == "dir"):
            name.setIcon(QIcon('../figures/dir.png'))
        else:
            name.setIcon(QIcon('../figures/file.png'))

#        modified = QTableWidgetItem(label[3])
#        self.setItem(write_row,3,modified)

    def RemoveAllRow(self):
        row = self.rowCount()
        print(">>>>row:",row)
        row -= 1
        while row >=0:
            self.removeRow(row)
            row -= 1

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.TopItemList = []

    def OpenAction(self):
        path = QFileDialog.getOpenFileName(self,"Open File Dialog",'',"image files(*.bin)")
        
        for index in self.TopItemList:
            if index.WinPath == path[0]:
                OpenFlag = True
                break
        else:
            OpenFlag = False

        if OpenFlag == False:
            item = TopItem(path[0])
            self.TopItemList.append(item)
            print(">>>>>>topitem",item)
            print(">>>>>>>self.tree",self.tree)
            print(">>>>>>self.TopItemList",self.TopItemList)
            self.tree.addTopLevelItem(item)
            self.LSRefresh(item)
            item.setExpanded(True)
        
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
        self.table.sortItems(0,Qt.AscendingOrder)
        self.tree = TreeWidget(self)
        self.tree.itemClicked.connect(self.TreeClick)
        
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.table)

        self.setCentralWidget(splitter)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('pyifs')
        self.show()

    def LSRefresh(self,item):
        index = item
        name = ""
        preName = ""

        while index.text(1) == "ChildItem":
            name = index.text(0) + "/" + preName
            preName = name
            print(">>>>>index.text(0)",index.text(0))
            index = index.parent()
        NameLen = len(name)
        if NameLen != 0:
            name = name[0:NameLen - 1]
        dir = bytes.decode(index.drive.path) + "/"
        print(">>>>>dir + name",(dir + name))
        entrys = index.drive.ls(dir + name)
        print(">>>>>entrys",entrys)
        self.table.RemoveAllRow()
        
        count = item.childCount()
        for var in entrys:
            name = bytes.decode(var[0])
            if "." in name:
                ls = name.split(".")
                suffix = ls[1].upper() + " "
            else:
                suffix = ""
                
            size = str(var[1])

            if (0x10 == var[2]):
                type = "dir"
                size = ""
                if count == 0:
                    item.addChild(ChildItem(name))
            else:
                type = suffix + "file"

            TableItemAttr = [name,size,type]
            self.table.AddItems(TableItemAttr)
            
    def TreeClick(self):
        item = self.tree.currentItem()
        print("-------------------------------treeclick------------------")
        print(">>>>>>item.text(0)",item.text(0))
        self.LSRefresh(item)
        item.setExpanded(True)

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    