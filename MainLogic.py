import fnmatch

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QTableWidgetItem
from MainWindow import Ui_MainWindow
from Resource import FileResource, NetworkResource
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtChart import QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtGui import QStandardItem

from LogBook import LogBook
from BlockBook import BlockBook
import re
import sys, os, pwd
import socket, struct


class MainWindowProgram(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.user_selector = ""
        self.file_selector = ""
        self.filesOpened = []
        self.socketsOpened = []
        self.socketsDict = {}
        self.all_user = False
        self.all_files = False
        self.user_reg = object()
        self.isFileMonitor = False
        self.PROC_SYS = "/proc/"
        self.TCP_SOURCE = '/proc/net/tcp'
        self.UDP_SOURCE = '/proc/net/udp'
        self.window_title = "Process Monitor"
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(lambda: self.startFilteringResource(logresult=True))
        self.MonitorButton.clicked.connect(self.updateMainWindow)
        self.IORadioButton.toggled.connect(self.checkSelection)
        self.NWRadioButton.toggled.connect(self.checkSelection)
        self.BackPushButton.clicked.connect(self.updateMainWindow)
        self.SaveDataPushButton.clicked.connect(self.saveDataToCSV)
        # self.usernamefilter = ''
        # self.processnamefilter = ''
        # self.genericfield1filter= ''
        # self.genericfield2filter= ''
        self.UserNameSearchText.textEdited.connect(self.setUserNameFilter)
        self.ProcessNameSearchText.textEdited.connect(self.setProcessNameFilter)
        self.GenericField1SearchText.textEdited.connect(self.setFilePathFilter)
        self.GenericField2SearchText.textEdited.connect(self.setAccessTimeFilter)
        self._translate = QCoreApplication.translate
        self.legacylogreader = LogBook()
        self.blockbook = BlockBook()
        self.blockbook.showWindow()
        self.userdata = dict()
        self.userbarsetdata = list()
        self.LegacyMonitorCheckBox.setChecked(False)
        self.AddUserNameToListView.clicked.connect(self.addUserToList)
        self.AddFileNameToListView.clicked.connect(self.addFileToList)
        self.RemoveUserButton.clicked.connect(self.removeUserFromList)
        self.RemoveFileButton.clicked.connect(self.removeFileFromList)

    def removeUserFromList(self):
        selectedId = self.UserListWidget.selectedItems()
        for i in selectedId:
            index = self.UserListWidget.indexFromItem(i)
            item = self.UserListWidget.takeItem(index.row())
            # print('removed item',item.text())
            if item.text() == '*':
                self.all_user = False

    def removeFileFromList(self):
        selectedId = self.FileListWidget.selectedItems()
        for i in selectedId:
            item = self.FileListWidget.takeItem(self.UserListWidget.indexFromItem(i).row())
            if item.text() == '*':
                self.all_files = False

    def addUserToList(self):
        username = self.UserNameText.text().strip()
        if not username or username == '*':
            self.all_user = True
            username = '*'
        self.UserListWidget.addItem(username)
        self.UserNameText.clear()

    def addFileToList(self):
        filename = self.FileDirectoryText.text().strip()
        if not filename or filename == '*':
            self.all_files = True
            filename = '*'
        self.FileListWidget.addItem(filename)
        self.FileDirectoryText.clear()

    def updateMainWindow(self):
        buttonPressed = self.sender().text()
        if buttonPressed == 'Back':
            self.timer.stop()
            self.MainStackedWidget.setCurrentIndex(0)
            self.legacylogreader.hidetable()
            self.setWindowTitle("Monitor")
        else:
            count = self.UserListWidget.count()
            if count == 0:
                self.all_user = True
                self.user_selector = ''
            else:
                # if count == 1:
                #     self.user_selector = self.UserListWidget.item(0).text()
                # else:
                found = False
                self.user_selector = list()
                for i in range(count):
                    user = self.UserListWidget.item(i).text()
                    if user == '*':
                        found = True
                        continue
                    user = '(' + user + ')'
                    self.user_selector.append(user)
                self.user_selector = '|'.join(self.user_selector)
                self.user_reg = re.compile(self.user_selector)
                self.all_user = found
            print('User Selector', self.user_selector, 'All Users?', self.all_user)
            if self.isFileMonitor:
                count = self.FileListWidget.count()
                self.file_selector = []
                if count == 0:
                    self.all_files = True
                else:
                    found = False
                    for i in range(count):
                        file = self.FileListWidget.item(i).text()
                        if file == '*':
                            found = True
                            continue
                        self.file_selector.append(file)
                    self.all_files = found
                print('File Selector', self.file_selector, 'All files?', self.all_files)
                self.setWindowTitle("File Monitor")
                self.MainStackedWidget.setCurrentIndex(1)
                self.GenericField1SearchText.setPlaceholderText(self._translate("FileStatisticsView", "File Path"))
                self.GenericField2SearchText.setPlaceholderText(self._translate("FileStatisticsView", "Access Time"))
                self.startFilteringResource(logresult=True)
                if self.LegacyMonitorCheckBox.isChecked():
                    self.legacylogreader.showtable(["File Path", "Access Time"], True, self.FSDTLabels)
            else:
                self.setWindowTitle("Network Monitor")
                self.MainStackedWidget.setCurrentIndex(1)
                self.GenericField1SearchText.setPlaceholderText(self._translate("NetStatisticsView", "Local Address"))
                self.GenericField2SearchText.setPlaceholderText(self._translate("NetStatisticsView", "Remote Address"))
                self.startFilteringResource(logresult=True)
                if self.LegacyMonitorCheckBox.isChecked():
                    self.legacylogreader.showtable(["Local Address", "Remote Address"], False, self.NTSDTLabels)
            self.timer.start()

    def updateuserstatisticschart(self):
        userseries = QBarSeries()
        self.StatisticQChart.removeAllSeries()
        for uname in self.userdata:
            barset = QBarSet(uname)
            barset.append(self.userdata[uname])
            userseries.append(barset)
        self.StatisticQChart.addSeries(userseries)
        categories = [" User Data"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        self.StatisticQChart.createDefaultAxes()
        self.StatisticQChart.setAxisX(axis, userseries)

    def setUserNameFilter(self, src):
        # self.usernamefilter = src
        # self.startFilteringResource()
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setFilterRegExp(src)

    def setProcessNameFilter(self, src):
        # self.processnamefilter = src
        # self.startFilteringResource()
        self.filter_proxy_model.setFilterKeyColumn(1)
        self.filter_proxy_model.setFilterRegExp(src)

    def setFilePathFilter(self, src):
        # self.genericfield1filter = src
        # self.startFilteringResource()
        self.filter_proxy_model.setFilterKeyColumn(2)
        self.filter_proxy_model.setFilterRegExp(src)

    def setAccessTimeFilter(self, src):
        # self.genericfield2filter = src
        # self.startFilteringResource()
        self.filter_proxy_model.setFilterKeyColumn(3)
        self.filter_proxy_model.setFilterRegExp(src)

    def checkSelection(self):
        if self.IORadioButton.isChecked():
            self.FileDirectoryLabel.setVisible(True)
            self.FileDirectoryText.setVisible(True)
            self.AddFileNameToListView.setVisible(True)
            self.isFileMonitor = True
        else:
            self.FileDirectoryLabel.setVisible(False)
            self.FileDirectoryText.setVisible(False)
            self.AddFileNameToListView.setVisible(False)
            self.isFileMonitor = False

    def getProcessFiles(self, proc, path, cmdline, uname, logresult):
        filterStrings = ['/dev/', 'socket:[', 'pipe', 'anon_inode:']
        for file in os.listdir(path + '/fd/'):
            found = record = False
            if self.isFileMonitor:
                if os.path.isfile(path + '/fd/' + file):
                    realfile = os.readlink(path + '/fd/' + file)
                    if os.path.isfile(realfile) or os.path.isdir(realfile):
                        for filter in filterStrings:
                            if filter in realfile:
                                found = True
                        if self.all_files and not found:
                            self.filesOpened.append(FileResource(proc, realfile, cmdline, uname))
                            record = True
                        else:
                            for file_selector_pattern in self.file_selector:
                                if fnmatch.fnmatch(realfile, file_selector_pattern):
                                    self.filesOpened.append(FileResource(proc, realfile, cmdline, uname))
                                    record = True
            else:
                try:
                    realfile = os.readlink(path + '/fd/' + file)
                    # print('Looking At:', realfile)
                    socketString = re.search('socket\:\[(\d+)\]', realfile)
                    if socketString:
                        # print('Looking for Socket#:', socketString.group())
                        socketNumber = socketString.group(1)
                        if self.socketsDict.get(socketNumber):
                            socket_info = self.socketsDict[socketNumber]
                            # local_addr_int = int(socket_info[0], 16)
                            # remote_addr_int = int(socket_info[1],16)
                            try:
                                # print('Found Socket Info:', self.socketsDict[socketNumber])
                                local_addr = socket_info[0].split(':')
                                local_ip = int(local_addr[0], 16)
                                local_port = int(local_addr[1], 16)
                                remote_addr = socket_info[1].split(':')
                                remote_ip = int(remote_addr[0], 16)
                                remote_port = int(remote_addr[1], 16)
                                local_addr = socket.inet_ntoa(struct.pack("<L", local_ip))
                                try:
                                    local_addr_dns = socket.gethostbyaddr(local_addr)[0]
                                except socket.herror:
                                    local_addr_dns = local_addr + ":" + str(local_port)
                                local_addr = local_addr + ":" + str(local_port)
                                remote_addr = socket.inet_ntoa(struct.pack("<L", remote_ip))
                                try:
                                    remote_addr_dns = socket.gethostbyaddr(remote_addr)[0]
                                except socket.herror:
                                    remote_addr_dns = remote_addr + ":" + str(remote_port)
                                remote_addr = remote_addr + ":" + str(remote_port)
                                self.socketsOpened.append(
                                    NetworkResource(proc, socketNumber, uname, cmdline, local_addr, local_addr_dns,
                                                    remote_addr, remote_addr_dns))
                                # print(local_addr_dns,remote_addr_dns)
                                record = True
                            except ValueError as e:
                                pass
                except FileNotFoundError:
                    pass
            if record:
                if logresult and uname in self.userdata:
                    self.userdata[uname] = self.userdata[uname] + 1
                else:
                    self.userdata[uname] = 1

    def saveDataToCSV(self):
        self.timer.stop()
        response = QFileDialog.getSaveFileName(self, 'Save to File', os.getcwd(), "Comma Separated File(*.csv)")
        if response[0]:
            file_name = response[0]
            if response[0].find('.csv') == -1:
                file_name = response[0] + ".csv"
            print('file: ', file_name)
            with open(file_name, 'w') as savefile:
                if self.isFileMonitor:
                    for resource in self.filesOpened:
                        savefile.write(str(resource) + '\n')
                else:
                    for resource in self.socketsOpened:
                        savefile.write(str(resource) + '\n')
        self.timer.start()

    def startFilteringResource(self, logresult=False):
        if self.isFileMonitor:
            self.getFileResouces(logresult)
        else:
            self.getNetResources(logresult)
        if logresult:
            self.updateuserstatisticschart()

    def getFileResouces(self, logresult):
        self.filesOpened.clear()
        self.datamodel.clear()
        self.datamodel.setHorizontalHeaderLabels(self.FSDTLabels)
        if logresult:
            self.userdata.clear()
        procs = os.listdir(self.PROC_SYS)
        for proc in procs:
            if proc.isnumeric():
                try:
                    st = os.stat(self.PROC_SYS + proc)
                    # print(self.PROC_SYS+proc,pwd.getpwuid(st.st_uid).pw_name)
                    if self.all_user or re.search(self.user_reg, pwd.getpwuid(st.st_uid).pw_name):
                        path = os.path.join(self.PROC_SYS, proc)
                        uname = pwd.getpwuid(st.st_uid).pw_name
                        # new_process = ProcessResource(proc,str(st.st_uid),os.path.join(self.PROC_SYS,proc))
                        with open(path + '/cmdline', 'r') as cmdlineFile:
                            cmdline = cmdlineFile.readline().strip().replace("\x00", " ")
                        self.getProcessFiles(proc, path, cmdline, uname, logresult)
                        # print('New Process:',new_process)
                        # print('\t Files:',new_process.files)
                except:
                    pass
        # for openedFile in self.filesOpened:
        #     print(openedFile)
        self.filesOpened.sort(key=lambda x: x.uname)
        if logresult:
            self.legacylogreader.addtologs(True, self.filesOpened)
        # print('Print size:', len(self.filesOpened))
        # if len(self.filesOpened):
        #     try:
        #         self.filesOpened = list(filter((lambda x: re.search(self.usernamefilter, x.uname)), self.filesOpened))
        #         self.filesOpened = list(filter((lambda x: re.search(self.processnamefilter, x.process)), self.filesOpened))
        #         self.filesOpened = list(filter((lambda x: re.search(self.genericfield1filter, x.path)), self.filesOpened))
        #         self.filesOpened = list(
        #             filter((lambda x: re.search(self.genericfield2filter, x.stime_access)), self.filesOpened))
        #     except:
        #         pass
        #
        # self.DataTable.clearContents()
        # self.DataTable.setRowCount(len(self.filesOpened))
        # self.DataTable.setSortingEnabled(False)
        # for file_count in range(len(self.filesOpened)):
        #     self.DataTable.setItem(file_count, 0, QTableWidgetItem(self.filesOpened[file_count].uname))
        #     self.DataTable.item(file_count,0).setToolTip(self.filesOpened[file_count].uname)
        #     self.DataTable.setItem(file_count, 1, QTableWidgetItem(self.filesOpened[file_count].process))
        #     self.DataTable.item(file_count, 1).setToolTip(self.filesOpened[file_count].process)
        #     self.DataTable.setItem(file_count, 2, QTableWidgetItem(self.filesOpened[file_count].path))
        #     self.DataTable.item(file_count, 2).setToolTip(self.filesOpened[file_count].path)
        #     self.DataTable.setItem(file_count, 3, QTableWidgetItem(self.filesOpened[file_count].stime_access))
        #     self.DataTable.item(file_count, 3).setToolTip(self.filesOpened[file_count].stime_access)
        # self.DataTable.setSortingEnabled(True)
        self.DataTable.setSortingEnabled(False)
        self.datamodel.setRowCount(len(self.filesOpened))
        for row, log in enumerate(self.filesOpened):
            item1 = QStandardItem(log.uname)
            item1.setToolTip(log.uname)
            self.datamodel.setItem(row, 0, item1)
            item2 = QStandardItem(log.process)
            item2.setToolTip(log.process)
            self.datamodel.setItem(row, 1, item2)
            item3 = QStandardItem(log.path)
            item3.setToolTip(log.path)
            self.datamodel.setItem(row, 2, item3)
            item4 = QStandardItem(log.stime_access)
            item4.setToolTip(log.stime_access)
            self.datamodel.setItem(row, 3, item4)
        self.DataTable.setSortingEnabled(True)

    def getNetResources(self, logresult):
        self.socketsOpened.clear()
        self.datamodel.clear()
        self.datamodel.setHorizontalHeaderLabels(self.NTSDTLabels)
        if logresult:
            self.userdata.clear()
        # self.user_selector = self.UserNameText.text().strip()
        # if not self.user_selector:
        #     self.all_user = True
        # else:
        #     self.all_user = False
        with open(self.TCP_SOURCE, 'r') as tcp:
            sockets = tcp.readlines()[1:]
            for socketline in sockets:
                addresses = socketline.strip().split()
                self.socketsDict[addresses[9]] = [addresses[1], addresses[2]]
                # local = addresses[1]
                # remote = addresses[2]
                # socket = addresses[10]
                # print(local, remote, socket)
        with open(self.UDP_SOURCE, 'r') as udp:
            sockets = udp.readlines()[1:]
            for socketline in sockets:
                addresses = socketline.strip().split()
                self.socketsDict[addresses[9]] = [addresses[1], addresses[2]]
        # print(self.socketsDict)
        procs = os.listdir(self.PROC_SYS)
        for proc in procs:
            if proc.isnumeric():
                try:
                    st = os.stat(self.PROC_SYS + proc)
                    # print(self.PROC_SYS+proc,pwd.getpwuid(st.st_uid).pw_name)
                    if self.all_user or re.search(self.user_reg, pwd.getpwuid(st.st_uid).pw_name):
                        path = os.path.join(self.PROC_SYS, proc)
                        uname = pwd.getpwuid(st.st_uid).pw_name
                        # new_process = ProcessResource(proc,str(st.st_uid),os.path.join(self.PROC_SYS,proc))
                        with open(path + '/cmdline', 'r') as cmdlineFile:
                            cmdline = cmdlineFile.readline().strip().replace("\x00", " ")
                        self.getProcessFiles(proc, path, cmdline, uname, logresult)
                        # print('New Process:',new_process)
                        # print('\t Files:',new_process.files)
                except:
                    pass
        # for openedFile in self.filesOpened:
        #     print(openedFile)
        self.socketsOpened.sort(key=lambda x: x.uname)
        if logresult:
            self.legacylogreader.addtologs(False, self.socketsOpened)
        # print('Print size:', len(self.socketsOpened))
        # if len(self.socketsOpened):
        #     try:
        #         self.socketsOpened = list(filter((lambda x: re.search(self.usernamefilter, x.uname)), self.socketsOpened))
        #         self.socketsOpened = list(filter((lambda x: re.search(self.processnamefilter, x.process)), self.socketsOpened))
        #         self.socketsOpened = list(filter((lambda x: re.search(self.genericfield1filter, x.local_addr)), self.socketsOpened))
        #         self.socketsOpened = list(filter((lambda x: re.search(self.genericfield2filter, x.remote_addr)), self.socketsOpened))
        #     except:
        #         pass
        #
        # self.DataTable.clearContents()
        # self.DataTable.setRowCount(len(self.socketsOpened))
        # self.DataTable.setSortingEnabled(False)
        # for file_count in range(len(self.socketsOpened)):
        #     self.DataTable.setItem(file_count, 0, QTableWidgetItem(self.socketsOpened[file_count].uname))
        #     self.DataTable.item(file_count, 0).setToolTip(self.socketsOpened[file_count].uname)
        #     self.DataTable.setItem(file_count, 1, QTableWidgetItem(self.socketsOpened[file_count].process))
        #     self.DataTable.item(file_count, 1).setToolTip(self.socketsOpened[file_count].process)
        #     self.DataTable.setItem(file_count, 2, QTableWidgetItem(self.socketsOpened[file_count].local_addr))
        #     self.DataTable.item(file_count, 2).setToolTip(self.socketsOpened[file_count].local_addr)
        #     self.DataTable.setItem(file_count, 3, QTableWidgetItem(self.socketsOpened[file_count].remote_addr))
        #     self.DataTable.item(file_count, 3).setToolTip(self.socketsOpened[file_count].remote_addr)
        #     # print(file_count,self.socketsOpened[file_count])
        # self.DataTable.setSortingEnabled(True)
        self.DataTable.setSortingEnabled(False)
        self.datamodel.setRowCount(len(self.socketsOpened))
        for row, log in enumerate(self.socketsOpened):
            item1 = QStandardItem(log.uname)
            item1.setToolTip(log.uname)
            self.datamodel.setItem(row, 0, item1)
            item2 = QStandardItem(log.process)
            item2.setToolTip(log.process)
            self.datamodel.setItem(row, 1, item2)
            item3 = QStandardItem(log.local_addr_dns)
            item3.setToolTip(log.local_addr)
            self.datamodel.setItem(row, 2, item3)
            item4 = QStandardItem(log.remote_addr_dns)
            item4.setToolTip(log.remote_addr)
            self.datamodel.setItem(row, 3, item4)
        self.DataTable.setSortingEnabled(True)


def main():
    app = QApplication(sys.argv)
    ui = MainWindowProgram()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
