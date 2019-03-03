# coding=utf-8

import paramiko
import threading


def main():
	
	ip = "192.168.2.109"
	port = 22
	username = "root"
	passwd = "carrot"

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip,username=user,password=passwd)

	ssh_session = client.get_transport().open_session()


if __name__ == '__main__':
	main()