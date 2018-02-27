from curses.ascii import isprint
import os
import datetime


class FileResource():
    def __init__(self,process_id, path,process,uname):
        self.process_id = process_id
        self.stat_result = os.stat(path)
        self.time_access = datetime.datetime.fromtimestamp(self.stat_result.st_atime)
        self.stime_access = self.time_access.strftime('%-m/%d/%Y - %H:%M:%S')
        self.path = path
        self.uname = uname
        self.process = process

    def __str__(self):
        return self.process_id+','+self.uname+','+self.process+','+self.path +','+self.stime_access

class NetworkResource():
    def __init__(self,process_id, socket_numb, uname, process,local_addr,local_addr_dns , remote_addr,remote_addr_dns):
        self.process_id = process_id
        self.socket_numb = socket_numb
        self.uname = uname
        self.process = process
        self.local_addr = local_addr
        self.local_addr_dns = local_addr_dns
        self.remote_addr = remote_addr
        self.remote_addr_dns = remote_addr_dns

    def __str__(self):
        return self.process_id+','+self.uname+','+self.process+','+self.local_addr +','+self.remote_addr

# class ProcessResource():
#     def __init__(self, pid, uid,path='',cmdline='',uname=''):
#         self.path = path
#         self.cmdline = cmdline
#         self.owner = ''
#         self.pid = pid
#         self.uid = uid
#         self.uname = uname if uname else pwd.getpwuid(int(uid)).pw_name
#
#     def __str__(self):
#         return self.cmdline +' - '+ self.pid + ' - ' + self.uname
