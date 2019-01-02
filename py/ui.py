# -*- coding:utf-8 -*-
import sys
import os
import pyifs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class TreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setColumnCount(1)
        self.setHeaderLabels([''])
        
    def AddTopItem(self,text):
        topLevelItem = QTreeWidgetItem()
        self.addTopLevelItem(topLevelItem)
        topLevelItem.setText(0,text)
        topLevelItem.setIcon(0,QIcon('../figures/dir.png'))
        return topLevelItem
    
    def AddSubItem(self,TopItem,text):
        subItem=QTreeWidgetItem(TopItem)
        subItem.setIcon(0,QIcon('../figures/dir.png'))
        subItem.setText(0,text)

        
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

    def ClickEvent(self):
        item=self.currentItem()

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

    def OpenAction(self):
        path = QFileDialog.getOpenFileName(self,"Open File Dialog",'',"image files(*.bin)")
        self.TopItem = self.tree.AddTopItem(os.path.basename(path[0]))
        #print(">>>>>>path[0]",path[0])
        self.drive = pyifs.pyifs(path[0])
        
        self.update(path[0],self.TopItem)
        
        self.TopItem.setExpanded(True)
        
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

    def update(self,dir_name,item):
        
        if (".") in dir_name:
            entry = self.drive.ls(dir + "/")
        else:
            entry = self.drive.ls(dir + "/" + dir_name)
        print(">>>>>entry",entry)
        self.table.RemoveAllRow()
        for index in entry:
            name = bytes.decode(index[0])
            if "." in name:
                ls = name.split(".")
                suffix = ls[1].upper() + " "
            else:
                suffix = ""
                
            size = str(index[1])

            if (0x10 == index[2]):
                type = "dir"
                size = ""
                self.tree.AddSubItem(item,name)
            else:
                type = suffix + "file"

            TableItem = [name,size,type]
            self.table.AddItems(TableItem)
            
    def TreeClick(self):
        LastTreeItem = None
        TreeItem=self.tree.currentItem()
        print(">>>>>>TreeItem:",TreeItem)
        print(">>>>>>TreeItem.text(0)",TreeItem.text(0))
        dir = bytes.decode(self.drive.path) + "/"
        index = TreeItem
        name = ""
        tempname = ""
        path = ""
        while self.TopItem != index:
            item = index.parent
            if self.TopItem == item:
                name += item.text(0)
                break
            else:
                tempname = "/" + index.text(0) + name
            index = item
        path = dir + name
        self.update(TreeItem.text(0),TreeItem)
        TreeItem.setExpanded(True)

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    