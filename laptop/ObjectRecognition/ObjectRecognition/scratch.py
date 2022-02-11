# coding:utf-8
# @des: Realize file upload, download and other functions


import paramiko
import os
import time
import datetime

host = "172.20.10.2"  # Remote server ip
user = "pi"  # Remote server username
password = "12345678"  # Remote server password
port = 22
local_put_path = "D:/ObjectRecognition/translate"  # The files that need to be uploaded are placed in this directory
#local_get_path = "D:/translate/camera"  # The files downloaded from the remote server are placed in this directory
remote_put_path = "/home/pi/Desktop/command/"  # The uploaded file is placed in this directory of the remote server
#remote_get_path = "/home/pi/Desktop/camera/"  # Download files from this directory on the remote server


def mkdir():

    for lp in [local_put_path, remote_put_path]:
        if not os.path.exists(lp):
            os.makedirs(lp, 666)
            print("创建本地文件夹:{}".format(lp))
        else:
            print("本地文件夹:{}已存在".format(lp))


class Pysftp(object):
 
    global local_put_path, remote_put_path

    def __init__(self, host, port, user, password):
        self.ssh = paramiko.SSHClient()
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
      
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.password)
        print("连接已建立")

    def cmd(self, cmd):
     
        # cmd = "date"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        #print(stdout.read().decode("utf8"))

    def put(self):
       
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        # sftp = self.ssh.open_sftp()
        for root, dirs, files in os.walk(local_put_path):
            for fname in files:
                local_full_name = os.path.join(root, fname)
                self.local_done_write(local_full_name)  # 本地文件已写入完成，可以上传了
                sftp.put(local_full_name, os.path.join(remote_put_path, fname))
                #os.remove(local_full_name)
                #print("{}\n上传成功：本地文件:{}====>远程{}:{}\n".format(datetime.datetime.now(), local_full_name,
                                                                       #self.host, remote_put_path))
            #time.sleep(10)

    #def get(self):
      
        #sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        # sftp = self.ssh.open_sftp() #  Open an sftp session on the ssh server
        #for fname in sftp.listdir(remote_get_path):
            #try:
                #   if fname.startswith('.py'):
                    #remote_full_name = os.path.join(remote_get_path, fname)
                    #self.remote_done_transffer(remote_full_name)
                    #sftp.get(remote_full_name, os.path.join(local_get_path, fname))
                    #sftp.remove(remote_full_name)
                    #print("[{}]下载成功：远程文件{}:{}====>本地{},已删除该远程文件\n".format(datetime.datetime.now(), self.host,
                                                                          #remote_full_name, local_get_path))
            #except Exception as e:
                #print(e)

    def stat(self, fpath):
    
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        # sftp = self.ssh.open_sftp()
        return sftp.stat(fpath)

    def remote_done_transffer(self, fpath):
 
        while True:
            old_size = self.stat(fpath).st_size
            time.sleep(1)
            new_size = self.stat(fpath).st_size
            if new_size <= old_size:  # Transfer completed
                return

    def close(self):
     
        self.ssh.close()
        print("Connection closed")

    def local_done_write(self, fpath):
    
        while True:
            old_size = os.stat(fpath).st_size
            time.sleep(0.01)
            new_size = os.stat(fpath).st_size
            if new_size <= old_size:  # Write completed
                return


def transffer():
 
    global host, port, user, password
    obj = Pysftp(host, port, user, password)
    obj.connect()
    mkdir()
    while True:
        # obj.cmd()
        obj.put()
        #time.sleep(10)


if __name__ == '__main__':
    transffer()
