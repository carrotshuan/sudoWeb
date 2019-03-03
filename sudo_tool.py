# coding=utf-8

import paramiko
import threading

def remote_target_execute(ip,port,username,passwd,command):

	ssh_session = paramiko.SSHClient()
	ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_session.connect(ip,port,username,passwd)

	stdin, stdout, stderr = ssh_session.exec_command(command)

	result = stdout.readlines()
	for line in result:
		print line,

	ssh_session.close()

def main():

	ip = "192.168.2.109"
	port = 22
	username = "root"
	passwd = "carrot"

	command = "ls"
	
	remote_target_execute(ip,port,username,passwd,command)


if __name__ == '__main__':
	main()
