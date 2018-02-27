import os
import sys
from PyQt5.QtWidgets import QLabel,QAbstractItemView,QMainWindow, QListWidget,QTableView, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import QCoreApplication,QSortFilterProxyModel, QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class BlockBook(QMainWindow):
    def __init__(self, parent=None, pwd=os.getcwd()):
        super(self.__class__, self).__init__(parent)
        self._translation = QCoreApplication.translate
        self.file_block_path ='/home/anand/LKM/file_ds'
        print(self.file_block_path)
        blockwidget = QWidget()
        blockvblayout = QGridLayout()
        blockfilenamelabel = QLabel()
        blockfilenamelabel.setText('File Name:')
        blockvblayout.addWidget(blockfilenamelabel, 0, 0)
        self.BlockFileNameLE = QLineEdit()
        self.BlockFileNameLE.setGeometry(QRect(0, 0, 50, 35))
        self.BlockFileNameLE.setObjectName("UserNameText")
        blockvblayout.addWidget(self.BlockFileNameLE, 0, 1)
        self.AddFileNameToListView = QPushButton()
        self.AddFileNameToListView.setObjectName("AddUserButton")
        self.AddFileNameToListView.setText('Add File')
        blockvblayout.addWidget(self.AddFileNameToListView, 0, 2)
        self.blockstate = False
        self.NWDirectoryLabel = QLabel()
        blockvblayout.addWidget(self.NWDirectoryLabel, 1, 0)
        self.NWDirectoryLabel.setText('Ip Address:')
        self.NWDirectoryText = QLineEdit()
        self.NWDirectoryText.setGeometry(QRect(0, 0, 200, 35))
        # self.NWDirectoryText.setObjectName("FileDirectoryText")
        blockvblayout.addWidget(self.NWDirectoryText, 1, 1)
        self.AddNWNameToListView = QPushButton()
        self.AddNWNameToListView.setText('Add Ip')
        # self.AddFileNameToListView.setObjectName("AddFileName")
        blockvblayout.addWidget(self.AddNWNameToListView, 1, 2)

        listviewrow = QHBoxLayout()
        self.FileListWidget = QListWidget()
        self.NWListWidget = QListWidget()
        self.FileListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.NWListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listviewrow.addWidget(self.FileListWidget)
        listviewrow.addWidget(self.NWListWidget)
        blockvblayout.addLayout(listviewrow, 3, 1)

        buttonrowlayout = QHBoxLayout()
        self.RemoveFileButton = QPushButton()
        self.RemoveFileButton.setText('Remove File(s)')
        self.RemoveNWButton = QPushButton()
        self.RemoveNWButton.setText('Remove Ip(s)')
        buttonrowlayout.addWidget(self.RemoveFileButton)
        buttonrowlayout.addWidget(self.RemoveNWButton)
        blockvblayout.addLayout(buttonrowlayout, 4, 1)
        buttonrowlayout2 = QHBoxLayout()
        self.BlockButton = QPushButton()
        self.BlockButton.setText('Block Resources')
        buttonrowlayout2.addWidget(self.BlockButton)
        blockvblayout.addLayout(buttonrowlayout2, 5, 1)
        blockwidget.setLayout(blockvblayout)
        self.setCentralWidget(blockwidget)
        self.setWindowTitle("Block Resouces")
        self.resize(800, 600)
        self.AddNWNameToListView.clicked.connect(self.addNWToList)
        self.AddFileNameToListView.clicked.connect(self.addFileToList)
        self.RemoveNWButton.clicked.connect(self.removeNWFromList)
        self.RemoveFileButton.clicked.connect(self.removeFileFromList)
        self.BlockButton.clicked.connect(self.blockorunblockresource)

    def removeNWFromList(self):
        selectedId = self.NWListWidget.selectedItems()
        for i in selectedId:
            self.NWListWidget.takeItem(self.NWListWidget.indexFromItem(i).row())

    def removeFileFromList(self):
        selectedId = self.FileListWidget.selectedItems()
        for i in selectedId:
            self.FileListWidget.takeItem(self.FileListWidget.indexFromItem(i).row())

    def addNWToList(self):
        nwIP = self.NWDirectoryText.text().strip()
        if not nwIP :
            return
        self.NWListWidget.addItem(nwIP)
        self.NWDirectoryText.clear()

    def addFileToList(self):
        filename = self.BlockFileNameLE.text().strip()
        if not filename:
            return
        self.FileListWidget.addItem(filename)
        self.BlockFileNameLE.clear()

    def blockorunblockresource(self):
        if self.blockstate:
            self.BlockButton.setText('Block Resource(s)')
            os.system('rmmod syscall')
            self.blockstate = False
        else:
            self.BlockButton.setText('Unblock Resource(s)')
            count = self.FileListWidget.count()
            with open(self.file_block_path,'w') as blockfile:
                for i in range(count):
                    file = self.FileListWidget.item(i).text()
                    blockfile.write(file+'\n')
            os.system('insmod /home/anand/LKM/syscall.ko')
            self.blockstate = True

    def hideWindow(self):
        self.hide()

    def showWindow(self):
        self.move(100,100)
        self.show()

def main():
    app = QApplication(sys.argv)
    block = BlockBook()
    block.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()