# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileStats.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileStatisticsView(QtWidgets.QVBoxLayout):
    def setupUi(self, FileStatisticsView):
        FileStatisticsView.setObjectName("FileStatisticsView")
        FileStatisticsView.resize(600, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FileStatisticsView)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.VerticalLayout = QtWidgets.QVBoxLayout()
        self.VerticalLayout.setObjectName("VerticalLayout")
        self.MainStackedWidget = QtWidgets.QStackedWidget(FileStatisticsView)
        self.MainStackedWidget.setObjectName("MainStackedWidget")
        self.StackedWidget = QtWidgets.QWidget()
        self.StackedWidget.setObjectName("StackedWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.StackedWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.DataTable = QtWidgets.QTableWidget(self.StackedWidget)
        self.DataTable.setWordWrap(False)
        self.DataTable.setCornerButtonEnabled(False)
        self.DataTable.setObjectName("DataTable")
        self.DataTable.setColumnCount(4)
        self.DataTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(3, item)
        self.DataTable.horizontalHeader().setCascadingSectionResizes(True)
        self.DataTable.horizontalHeader().setSortIndicatorShown(True)
        self.DataTable.horizontalHeader().setStretchLastSection(True)
        self.DataTable.verticalHeader().setCascadingSectionResizes(True)
        self.DataTable.verticalHeader().setSortIndicatorShown(True)
        self.DataTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout_3.addWidget(self.DataTable)
        self.MainStackedWidget.addWidget(self.StackedWidget)
        self.VerticalLayout.addWidget(self.MainStackedWidget)
        self.verticalLayout_2.addLayout(self.VerticalLayout)
        self.horzontalLayout = QtWidgets.QHBoxLayout()
        self.horzontalLayout.setObjectName("horzontalLayout")
        self.UserNameSearchText = QtWidgets.QLineEdit(FileStatisticsView)
        self.UserNameSearchText.setObjectName("UserNameSearchText")
        self.horzontalLayout.addWidget(self.UserNameSearchText)
        self.ProcessNameSearchText = QtWidgets.QLineEdit(FileStatisticsView)
        self.ProcessNameSearchText.setObjectName("ProcessNameSearchText")
        self.horzontalLayout.addWidget(self.ProcessNameSearchText)
        self.FilePathSearchText = QtWidgets.QLineEdit(FileStatisticsView)
        self.FilePathSearchText.setObjectName("FilePathSearchText")
        self.horzontalLayout.addWidget(self.FilePathSearchText)
        self.AccessTimeSearchText = QtWidgets.QLineEdit(FileStatisticsView)
        self.AccessTimeSearchText.setObjectName("AccessTimeSearchText")
        self.horzontalLayout.addWidget(self.AccessTimeSearchText)
        self.verticalLayout_2.addLayout(self.horzontalLayout)
        self.FSDTLabels = []
        self.NTSDTLabels = []

        self.retranslateUi(FileStatisticsView)
        QtCore.QMetaObject.connectSlotsByName(FileStatisticsView)

    def retranslateUi(self, FileStatisticsView):
        _translate = QtCore.QCoreApplication.translate
        FileStatisticsView.setWindowTitle(_translate("FileStatisticsView", "Form"))
        self.DataTable.setSortingEnabled(True)
        self.DataTable.setHorizontalHeaderLabels()
        self.FSDTLabels.append(_translate("FileStatisticsView", "User Name"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "Process Name"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "File Path"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "Access Time"))
        self.UserNameSearchText.setPlaceholderText(_translate("FileStatisticsView", "User Name"))
        self.ProcessNameSearchText.setPlaceholderText(_translate("FileStatisticsView", "Process Name"))
        self.FilePathSearchText.setPlaceholderText(_translate("FileStatisticsView", "File Path"))
        self.AccessTimeSearchText.setPlaceholderText(_translate("FileStatisticsView", "Access Time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FileStatisticsView = QtWidgets.QWidget()
    ui = Ui_FileStatisticsView()
    ui.setupUi(FileStatisticsView)
    FileStatisticsView.show()
    sys.exit(app.exec_())

