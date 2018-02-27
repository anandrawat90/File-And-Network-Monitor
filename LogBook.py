import os
import sys
from PyQt5.QtWidgets import QMainWindow, QTableView, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import QCoreApplication,QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class LogBook(QMainWindow):
    def __init__(self,parent = None, pwd = os.getcwd()):
        super(self.__class__, self).__init__(parent)
        self._translation = QCoreApplication.translate
        self.file_log_path = str(pwd) + '/' + 'legacy_file_log.csv'
        self.net_log_path = str(pwd) + '/' + 'legacy_net_log.csv'
        print(self.file_log_path, self.net_log_path)
        statisticswidget = QWidget()
        statisticswidget.setObjectName("legacy_statisticswidget")
        statisticvlayout = QVBoxLayout()
        statisticvlayout.setObjectName("legacy_statisticvlayout")
        horizontallayout = QHBoxLayout()
        horizontallayout.setContentsMargins(0, 0, 0, 0)
        horizontallayout.setObjectName("legacy_horizontalLayout")
        self.model = QStandardItemModel(0, 4)
        self.LegacyTableView = QTableView()
        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.LegacyTableView.setModel(self.filter_proxy_model)
        self.LegacyTableView.setCornerButtonEnabled(False)
        self.LegacyTableView.setObjectName("LegacyTableView")
        self.LegacyTableView.resizeColumnsToContents()
        self.LegacyTableView.setWordWrap(True)
        self.LegacyTableView.setSortingEnabled(True)
        self.LegacyTableView.horizontalHeader().setCascadingSectionResizes(True)
        self.LegacyTableView.horizontalHeader().setSortIndicatorShown(True)
        self.LegacyTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.LegacyTableView.verticalHeader().setCascadingSectionResizes(True)
        self.LegacyTableView.verticalHeader().setSortIndicatorShown(True)
        self.LegacyTableView.verticalHeader().setVisible(False)
        self.UserNameSearchText = QLineEdit()
        self.UserNameSearchText.setObjectName("legacy_UserNameSearchText")
        horizontallayout.addWidget(self.UserNameSearchText)
        self.ProcessNameSearchText = QLineEdit()
        self.ProcessNameSearchText.setObjectName("legacy_ProcessNameSearchText")
        horizontallayout.addWidget(self.ProcessNameSearchText)
        self.GenericField1SearchText = QLineEdit()
        self.GenericField1SearchText.setObjectName("legacy_FilePathSearchText")
        horizontallayout.addWidget(self.GenericField1SearchText)
        self.GenericField2SearchText = QLineEdit()
        self.GenericField2SearchText.setObjectName("legacy_AccessTimeSearchText")
        self.UserNameSearchText.setPlaceholderText(self._translation("FileStatisticsView", "User Name"))
        self.ProcessNameSearchText.setPlaceholderText(self._translation("FileStatisticsView", "Process Name"))
        self.UserNameSearchText.textEdited.connect(self.setUserNameFilter)
        self.ProcessNameSearchText.textEdited.connect(self.setProcessNameFilter)
        self.GenericField1SearchText.textEdited.connect(self.setFilePathFilter)
        self.GenericField2SearchText.textEdited.connect(self.setAccessTimeFilter)
        horizontallayout.addWidget(self.GenericField2SearchText)
        statisticvlayout.addWidget(self.LegacyTableView)
        statisticvlayout.addLayout(horizontallayout)
        statisticswidget.setLayout(statisticvlayout)
        self.setCentralWidget(statisticswidget)
        self.setWindowTitle("Legacy Log Monitor")
        self.resize(800,600)
        self.filelogset = set()
        self.netlogset = set()
        file_logs = list()
        if os.path.isfile(self.file_log_path):
            with open(self.file_log_path, 'r') as legacy_log:
                file_logs = legacy_log.readlines()
        self.file_log_count = len(file_logs)
        for log in file_logs:
            record = log.strip()
            self.filelogset.add(record)
        net_logs = list()
        if os.path.isfile(self.net_log_path):
            with open(self.net_log_path, 'r') as legacy_log:
                net_logs = legacy_log.readlines()
        self.net_log_count = len(net_logs)
        for log in net_logs:
            record = log.strip()
            self.netlogset.add(record)

    def addtologs(self,file_monitor,records):
        log_set = self.filelogset if file_monitor else self.netlogset
        log_path = self.file_log_path if file_monitor else self.net_log_path
        with open(log_path, 'a') as legacy_log:
            for record in records:
                entry = str(record)
                if entry not in log_set:
                    log_set.add(entry)
                    legacy_log.write(entry+"\n")

    def loadlegacyfilelogs(self, isfilemonitor):
        logset = self.filelogset if isfilemonitor else self.netlogset
        self.model.setRowCount(len(logset))
        self.LegacyTableView.setSortingEnabled(False)
        for row, log in enumerate(logset):
            record = log.split(',')
            item1 = QStandardItem(record[1])
            item1.setToolTip(record[1])
            self.model.setItem(row, 0, item1)
            item2 = QStandardItem(record[2])
            item2.setToolTip(record[2])
            self.model.setItem(row, 1, item2)
            item3 = QStandardItem(record[3])
            item3.setToolTip(record[2])
            self.model.setItem(row, 2, item3)
            item4 = QStandardItem(record[4])
            item4.setToolTip(record[4])
            self.model.setItem(row, 3, item4)
        self.LegacyTableView.setSortingEnabled(True)

    def showtable(self,placeholders,isfilemonitor, labels):
        self.GenericField1SearchText.setPlaceholderText(self._translation("FileStatisticsView", placeholders[0]))
        self.GenericField2SearchText.setPlaceholderText(self._translation("FileStatisticsView", placeholders[1]))
        self.model.clear()
        self.model.setHorizontalHeaderLabels(labels)
        self.move(100,100)
        self.loadlegacyfilelogs(isfilemonitor)
        self.show()

    def hidetable(self):
        self.hide()

    def setUserNameFilter(self, src):
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setFilterRegExp(src)

    def setProcessNameFilter(self, src):
        self.filter_proxy_model.setFilterKeyColumn(1)
        self.filter_proxy_model.setFilterRegExp(src)

    def setFilePathFilter(self, src):
        self.filter_proxy_model.setFilterKeyColumn(2)
        self.filter_proxy_model.setFilterRegExp(src)

    def setAccessTimeFilter(self, src):
        self.filter_proxy_model.setFilterKeyColumn(3)
        self.filter_proxy_model.setFilterRegExp(src)


def main():
    app = QApplication(sys.argv)
    log = LogBook(pwd='/home/anandrawat/CSC_239/Simple Qt5/')
    log.showtable(['File Path', 'Access Time'],True, ["User Name","Process Name","File Path","Access Time"])
    log.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()