# -*- coding:utf-8 -*-
import sys
import os
import pyifs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class tableNameItem(QTableWidgetItem):
    def __init__(self,text,imgPath):
        super().__init__()
        
        self.setText(text)
        self.imgPath = imgPath

        
class TreeTopItem(QTreeWidgetItem):
    def __init__(self,path):
        super().__init__()

        self.drive = pyifs.pyifs(path)
        self.winPath = path
        self.imgPath = bytes.decode(self.drive.path) + "/"
        self.setText(0,os.path.basename(path))
        self.setText(1,"TreeTopItem")
        self.setIcon(0,QIcon('../figures/dir.png'))
    
class TreeChildItem(QTreeWidgetItem):
    def __init__(self,text,imgPath):
        super().__init__()
        self.imgPath = imgPath
        self.setText(0,text)
        self.setText(1,"TreeChildItem")
        self.setIcon(0,QIcon('../figures/dir.png'))
        self.setExpanded(True)
        
class TreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setColumnCount(1)
        self.setHeaderLabels([''])
    
    def getTreeItemDir(self,item):
        index = item
        name = ""
        preName = ""

        while index.text(1) == "TreeChildItem":
            name = index.text(0) + "/" + preName
            preName = name
            print(">>>>>index.text(0)",index.text(0))
            index = index.parent()
        NameLen = len(name)
        if NameLen != 0:
            name = name[0:NameLen - 1]
        topItem = index
        dir = topItem.imgPath + name
        
        return topItem,dir
    
    def refreshTree(self,dirList):
        item = self.currentItem()
        
        count = item.childCount()
        if count == 0:
            for index in dirList:
                item.addChild(TreeChildItem(index[0],index[3]))
        
class TableWidget(QTableWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent;
        self.fileList = []
        self.dirList = []
        self.sortDir = False
        self.setColumnCount(4)
        self.horizontalHeader().sectionClicked.connect(self.onTableHeaderClick)
        
        text = ['Name','Size','Type','Modified']
        for index in range(4):
            item = QTableWidgetItem(text[index])
            self.setHorizontalHeaderItem(index,item)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setShowGrid(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def clearAllList(self):
        self.fileList = []
        self.dirList = []

    def addTableItems(self):
        self.removeAllRow()
        tableList = self.dirList + self.fileList
        for index in tableList:
            write_row = self.rowCount()
            self.setRowCount(self.rowCount()+1)
            name = tableNameItem(index[0],index[3])
            self.setItem(write_row,0,name)
            
            size = QTableWidgetItem(index[1])
            self.setItem(write_row,1,size)
            
            type = QTableWidgetItem(index[2])
            self.setItem(write_row,2,type)
            
            if (index[2] == "dir"):
                name.setIcon(QIcon('../figures/dir.png'))
            else:
                name.setIcon(QIcon('../figures/file.png'))

#        modified = QTableWidgetItem(label[3])
#        self.setItem(write_row,3,modified)

    def removeAllRow(self):
        row = self.rowCount()
        print(">>>>row:",row)
        row -= 1
        while row >=0:
            self.removeRow(row)
            row -= 1

    def onTableHeaderClick(self,column):
        #item = self.table.currentItem()
        print(">>>>>>click colume:",column)
        
        if column == 0:
            self.nameOrTypeSort(column)
        elif column == 1:
            self.sizeSort()
        elif column == 2:
            self.nameOrTypeSort(column)

    def nameOrTypeSort(self,column,changDir=True):
        if self.sortDir == False:
            self.fileList.sort(key=lambda ele:ele[column].lower())
            self.dirList.sort(key=lambda ele:ele[column].lower())
            if changDir == True:
                self.sortDir = True
        else:
            self.fileList.sort(key=lambda ele:ele[column].lower(),reverse=True)
            self.dirList.sort(key=lambda ele:ele[column].lower(),reverse=True)
            if changDir == True:
                self.sortDir = False
        self.addTableItems()

    def sizeSort(self):
        if self.sortDir == False:
            self.fileList.sort(key=lambda ele:int(ele[1]))
            self.sortDir = True
        else:
            self.fileList.sort(key=lambda ele:int(ele[1]),reverse=True)
            self.sortDir = False
        self.addTableItems()
        
    def refreshTable(self,entrys,dir):
        self.clearAllList()

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
            else:
                type = suffix + "file"
            imgPath = dir + name
            TableItemAttr = [name,size,type,imgPath]
            if type == "dir":
                self.dirList.append(TableItemAttr)
            else:
                self.fileList.append(TableItemAttr)

        self.nameOrTypeSort(0,False)
        
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.TopItemList = []

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
 
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open image')
        openAction.triggered.connect(self.openAction)
 
        self.statusBar()
 
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)
        
        self.table = TableWidget(self)
        self.tree = TreeWidget(self)
        self.tree.itemClicked.connect(self.onTreeItemClicked)
        self.table.cellDoubleClicked.connect(self.onTableCellDoubleClicked)
        
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.table)

        self.setCentralWidget(splitter)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('pyifs')
        self.show()

    def openAction(self):
        path = QFileDialog.getOpenFileName(self,"Open File Dialog",'',"image files(*.bin)")
        
        for index in self.TopItemList:
            if index.winPath == path[0]:
                OpenFlag = True
                break
        else:
            OpenFlag = False

        if OpenFlag == False:
            item = TreeTopItem(path[0])
            self.TopItemList.append(item)
            self.tree.addTopLevelItem(item)

            self.tree.setCurrentItem(item)
            entrys = item.drive.ls(item.imgPath)
            print(">>>>entrys:",entrys)
            item.setExpanded(True)
            self.table.refreshTable(entrys,item.imgPath)
            self.tree.refreshTree(self.table.dirList)
            TreeItem = self.tree.currentItem()
            print(">>>>>>>>>>>openAction>>>self.tree.currentItem():",TreeItem)
            if TreeItem!= None:
                print(">>>>>>TreeItem.text()",TreeItem.text(0))
        
    def onTreeItemClicked(self):
        item = self.tree.currentItem()
        print(">>>>>>>>>>>onTreeItemClick>>>>self.tree.currentItem():",item)
        #result = self.tree.getTreeItemDir(item)
        #print(">>>>>onTreeItemClicked>>>>topitem",result[0])
        #print(">>>>>onTreeItemClicked>>>>TreeItemDir",result[1])
        dir = item.imgPath[0:3]
        for topItem in self.TopItemList:
            if dir == topItem.imgPath:
                break;
        entrys = topItem.drive.ls(item.imgPath)
        self.table.refreshTable(entrys,item.imgPath)
        self.tree.refreshTree(self.table.dirList)
        item.setExpanded(True)

    def onTableCellDoubleClicked(self,row,column):
        item = self.tree.currentItem()
        print(">>>>>>>>>>>onTableCellDoubleClicked>>>>self.tree.currentItem():",item)
        print(">>>>>>>>row:",row)
        print(">>>>>>>>column:",column)
        item = self.table.item(row,column)
        print(">>>>>item.text():",item.text())

if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    