# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QApplication, QMainWindow, QTableView, QRadioButton, \
    QPushButton, QStackedWidget, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QCheckBox, QListWidget, QAbstractItemView
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication, QRect, QMargins, QSortFilterProxyModel
from PyQt5.QtGui import QPainter, QStandardItemModel


class Ui_MainWindow(object):
    # def __init__(self):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.MainInterfaceGridLayout = QGridLayout()
        self.MainStackedWidget = QStackedWidget(MainWindow)
        self.LoginCenterWidget = QWidget()
        self.UserNameLabel = QLabel()
        self.MainStackedWidget.setObjectName("MainStackedWidget")
        self.MainInterfaceGridLayout.setSpacing(5)
        self.MainInterfaceGridLayout.setAlignment(Qt.AlignCenter)
        self.LoginCenterWidget.setObjectName("LoginCenterWidget")
        # self.UserNameLabel.setGeometry(QtCore.QRect(240, 200, 91, 31))
        self.MainInterfaceGridLayout.addWidget(self.UserNameLabel, 0, 0)
        self.UserNameLabel.setObjectName("UserNameLabel")
        self.UserNameText = QLineEdit()
        self.UserNameText.setGeometry(QRect(0, 0, 50, 35))
        self.UserNameText.setObjectName("UserNameText")
        self.MainInterfaceGridLayout.addWidget(self.UserNameText, 0, 1)

        self.AddUserNameToListView = QPushButton()
        self.AddUserNameToListView.setObjectName("AddUserButton")
        self.MainInterfaceGridLayout.addWidget(self.AddUserNameToListView, 0, 2)

        # Logic for specifying File Directory
        self.FileDirectoryLabel = QLabel()
        self.MainInterfaceGridLayout.addWidget(self.FileDirectoryLabel, 1, 0)
        self.FileDirectoryLabel.setObjectName("FileDirectoryLabel")
        self.FileDirectoryText = QLineEdit()
        self.FileDirectoryText.setGeometry(QRect(0, 0, 200, 35))
        self.FileDirectoryText.setObjectName("FileDirectoryText")
        self.MainInterfaceGridLayout.addWidget(self.FileDirectoryText, 1, 1)
        self.FileDirectoryLabel.setVisible(False)
        self.FileDirectoryText.setVisible(False)
        self.AddFileNameToListView = QPushButton()
        self.AddFileNameToListView.setVisible(False)
        self.AddFileNameToListView.setObjectName("AddFileName")
        self.MainInterfaceGridLayout.addWidget(self.AddFileNameToListView, 1, 2)

        rowlayout = QHBoxLayout()
        self.IORadioButton = QRadioButton()
        # self.IORadioButton.setGeometry(QtCore.QRect(240, 240, 161, 22))
        self.IORadioButton.setObjectName("IORadioButton")
        self.NWRadioButton = QRadioButton()
        # self.NWradioButton.setGeometry(QtCore.QRect(416, 240, 161, 22))
        self.NWRadioButton.setObjectName("NWradioButton")
        self.NWRadioButton.setChecked(True)
        rowlayout.addWidget(self.NWRadioButton)
        rowlayout.addWidget(self.IORadioButton)
        self.LegacyMonitorCheckBox = QCheckBox()
        self.LegacyMonitorCheckBox.setObjectName('LegacyMonitorCheckBox')
        rowlayout.addWidget(self.LegacyMonitorCheckBox)
        self.MainInterfaceGridLayout.addLayout(rowlayout, 2, 1)

        listviewrow = QHBoxLayout()
        self.UserListWidget = QListWidget()
        self.FileListWidget = QListWidget()
        self.UserListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.FileListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.MonitorButton = QPushButton()
        listviewrow.addWidget(self.UserListWidget)
        listviewrow.addWidget(self.FileListWidget)
        self.MainInterfaceGridLayout.addLayout(listviewrow, 3, 1)

        buttonrowlayout = QHBoxLayout()
        self.RemoveUserButton = QPushButton()
        self.RemoveFileButton = QPushButton()
        buttonrowlayout.addWidget(self.RemoveUserButton)
        buttonrowlayout.addWidget(self.RemoveFileButton)
        self.MainInterfaceGridLayout.addLayout(buttonrowlayout,4,1)

        # SpacerItem = QSpacerItem(0,0)
        # self.GridLayout.addItem(SpacerItem,2,0)
        self.MainInterfaceGridLayout.addWidget(self.MonitorButton, 5, 1)
        # self.MonitorButton.setGeometry(QtCore.QRect(238, 270, 351, 27))
        self.MonitorButton.setObjectName("MonitorButton")
        self.LoginCenterWidget.setLayout(self.MainInterfaceGridLayout)
        self.MainStackedWidget.insertWidget(0, self.LoginCenterWidget)

        '''Navigation Menu and Save Controls'''
        self.NavigationHorzontalLayout = QHBoxLayout()
        self.BackPushButton = QPushButton()
        self.BackPushButton.setObjectName("BushPushButton")
        self.SaveDataPushButton = QPushButton()
        self.SaveDataPushButton.setObjectName("SaveDataPushButton")
        self.NavigationHorzontalLayout.addWidget(self.BackPushButton)
        self.NavigationHorzontalLayout.addWidget(self.SaveDataPushButton)

        ''' Statistics Layout '''
        self.StatisticsWidget = QWidget()
        self.StatisticVLayout = QVBoxLayout()
        self.StatisticVLayout.setObjectName("StatisticVLayout")
        # Statistics Chart
        self.StatisticQChart = QChart()
        self.StatisticQChart.setObjectName("StatisticQChart")
        self.StatisticQChart.setTitle("User Statistics")
        self.StatisticQChart.setAnimationOptions(QChart.NoAnimation)
        self.StatisticQChart.setMargins(QMargins(2, 2, 2, 2))
        self.StatisticQChart.legend().setVisible(True)
        self.StatisticQChart.legend().setAlignment(Qt.AlignBottom)
        self.StatisticQChart.setTheme(QChart.ChartThemeBlueCerulean)
        self.StatisticQChartView = QChartView(self.StatisticQChart)
        self.StatisticQChartView.setRenderHint(QPainter.Antialiasing)
        self.StatisticVLayout.addWidget(self.StatisticQChartView)
        # Data table Constuction
        self.DataTable = QTableView()
        self.DataTable.setCornerButtonEnabled(False)
        self.DataTable.setObjectName("DataTable")
        # self.DataTable.setColumnCount(4)
        # self.DataTable.setRowCount(0)
        self.datamodel = QStandardItemModel(0, 4)
        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.datamodel)
        self.DataTable.setModel(self.filter_proxy_model)
        self.DataTable.resizeColumnsToContents()
        self.DataTable.setWordWrap(True)
        self.DataTable.setSortingEnabled(True)
        # self.DataTable.setHorizontalHeaderItem(0, QTableWidgetItem('Field 1'))
        # self.DataTable.setHorizontalHeaderItem(1, QTableWidgetItem('Field 2'))
        # self.DataTable.setHorizontalHeaderItem(2, QTableWidgetItem('Field 3'))
        # self.DataTable.setHorizontalHeaderItem(3, QTableWidgetItem('Field 4'))
        self.DataTable.horizontalHeader().setCascadingSectionResizes(True)
        self.DataTable.horizontalHeader().setSortIndicatorShown(True)
        self.DataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DataTable.verticalHeader().setCascadingSectionResizes(True)
        self.DataTable.verticalHeader().setSortIndicatorShown(True)
        self.DataTable.verticalHeader().setVisible(False)
        # Adding data table to vertical layout
        self.StatisticVLayout.addWidget(self.DataTable)
        horzontalLayout = QHBoxLayout()
        horzontalLayout.setObjectName("horzontalLayout")
        self.UserNameSearchText = QLineEdit()
        self.UserNameSearchText.setObjectName("UserNameSearchText")
        horzontalLayout.addWidget(self.UserNameSearchText)
        self.ProcessNameSearchText = QLineEdit()
        self.ProcessNameSearchText.setObjectName("ProcessNameSearchText")
        horzontalLayout.addWidget(self.ProcessNameSearchText)
        self.GenericField1SearchText = QLineEdit()
        self.GenericField1SearchText.setObjectName("FilePathSearchText")
        horzontalLayout.addWidget(self.GenericField1SearchText)
        self.GenericField2SearchText = QLineEdit()
        self.GenericField2SearchText.setObjectName("AccessTimeSearchText")
        horzontalLayout.addWidget(self.GenericField2SearchText)

        self.StatisticVLayout.addLayout(horzontalLayout)
        self.StatisticVLayout.addLayout(self.NavigationHorzontalLayout)
        self.StatisticsWidget.setLayout(self.StatisticVLayout)
        self.MainStackedWidget.insertWidget(1, self.StatisticsWidget)

        MainWindow.setCentralWidget(self.MainStackedWidget)
        MainWindow.setGeometry(100, 100, 800, 600)
        self.FSDTLabels = list()
        self.NTSDTLabels = list()
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.UserNameLabel.setText(_translate("MainWindow", "User Name:"))
        self.FileDirectoryLabel.setText(_translate("MainWindow", "File Directory:"))
        self.IORadioButton.setText(_translate("MainWindow", "Input / Output"))
        self.NWRadioButton.setText(_translate("MainWindow", "Network"))
        self.MonitorButton.setText(_translate("MainWindow", "Monitor"))
        self.LegacyMonitorCheckBox.setText(_translate("MainWindow", "Show Legacy Monitor"))
        self.AddUserNameToListView.setText(_translate("MainWindow","Add User"))
        self.AddFileNameToListView.setText(_translate("MainWindow","Add File"))
        self.RemoveUserButton.setText(_translate("MainWindow","Remove User(s)"))
        self.RemoveFileButton.setText(_translate("MainWindow","Remove File(s)"))
        '''Navigation and Save Options'''
        self.BackPushButton.setText(_translate("Navigation", "Back"))
        self.SaveDataPushButton.setText(_translate("Navigation", "Save Data"))
        '''File Statistics'''
        self.FSDTLabels.append(_translate("FileStatisticsView", "User Name"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "Process Name"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "File Path"))
        self.FSDTLabels.append(_translate("FileStatisticsView", "Access Time"))

        '''Network Statistics'''
        self.NTSDTLabels.append(_translate("NetStatisticsView", "User Name"))
        self.NTSDTLabels.append(_translate("NetStatisticsView", "Process Name"))
        self.NTSDTLabels.append(_translate("NetStatisticsView", "Local Address"))
        self.NTSDTLabels.append(_translate("NetStatisticsView", "Remote Address"))

        self.DataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.DataTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.UserNameSearchText.setPlaceholderText(_translate("FileStatisticsView", "User Name"))
        self.ProcessNameSearchText.setPlaceholderText(_translate("FileStatisticsView", "Process Name"))

    def updatestackedframe(self, index):
        self.MainStackedWidget.setCurrentIndex(index)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.updatestackedframe(1)
    sys.exit(app.exec_())
