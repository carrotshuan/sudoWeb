# coding=utf-8

import hashlib
import difflib
import sys
import os
import configparser
import re
import time


# 显示颜色
color_red_start = "\033[0;31;40m"
color_green_start = "\033[0;32;40m"
color_yellow_start = "\033[0;33;40m"

color_end = "\033[0m"

conf = configparser.ConfigParser()
conf.read("sysconfig.conf")

work_root_path = os.getcwd()

# 判断给定字符串是否是IP
def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$')
    if p.match(str):
        return True
    else:
        return False

# 所有以主机命名的文件夹数据所在的上级目录
def get_hosts_to_merge_abs_path():

	hosts_to_merge_abspath = work_root_path + "/" + conf.get("local","hosts_to_merge_dirname")
	return hosts_to_merge_abspath

# sudo脚本数据库所在的目录的全路径
def get_scriptDB_abs_path():

	db_dir_abspath = work_root_path + "/" + conf.get("local","sudo_db_dirname")

	return db_dir_abspath

# 获取每个主机ip目录下的待分析脚本目录名
def get_sudo_script_dirname():

	ip_scripts_dirname = conf.get("local","ip_scripts_dirname")

	return ip_scripts_dirname

# 返回每个待分析主机目录和脚本目录的全路径
def get_all_hosts_scripts_dirname_to_merge_abspath():

	all_hosts_to_merge = []
	hosts_directorys = os.listdir(get_hosts_to_merge_abs_path())

	for directory in hosts_directorys:
		# 过滤以.开头的非待分析数据文件夹
		if isIP(directory):
			all_hosts_to_merge.append(directory)

	all_hosts_to_merge_abspath = []

	# 将上面得到的路径转换为全路径
	for host in all_hosts_to_merge:
		all_hosts_to_merge_abspath.append(get_hosts_to_merge_abs_path()+"/"+host+"/"+get_sudo_script_dirname())

	return all_hosts_to_merge_abspath


# 计算单个文件的MD5值并返回
def calculate_MD5(filepath):
	with open(filepath,'rb') as f:
		md5obj = hashlib.md5()
		md5obj.update(f.read())
		hash = md5obj.hexdigest()
		# print "Hash of " + filepath + " is: " + hash
		return hash


# # 根据hash值是否一致，检查文件是否在目录中
# def check_file_in_directory(file_fullpath,directory_fullpath):

# 	current_db_scripts_names = os.listdir(directory_fullpath) # 当前sudo 脚本数据库中脚本文件名
# 	# print "current_db_scripts_names: ",current_db_scripts_names	
	
# 	corresponding_hash_value = []

# 	for file_name in current_db_scripts_names:
# 		file_abs_path = directory_fullpath+"/"+file_name

# 		corresponding_hash_value.append(file_abs_path)

# # 将单个sudo脚本放入sudo数据库
# def merge_single_script_to_sudo_database(single_sudo_script_fullpath):

# 	script_path = single_sudo_script_fullpath[0:single_sudo_script_fullpath.rfind("/")]
# 	script_name = single_sudo_script_fullpath.split("/")[-1]
# 	print "current merging filename: " + script_name


# 将源文件夹中的文件，合并到目标文件夹中，相同文件不需合并，不同文件拷贝到目标文件中
def merge_two_directory_directly(source_directory_fullpath, target_directory_fullpath):

		# 分别获取两个目录下的文件名，非全路径
		source_file_names = os.listdir(source_directory_fullpath)
		target_file_names = os.listdir(target_directory_fullpath)

		# 分别将以上获取文件名转换为全路径文件名
		source_file_names_fullpath = []
		target_file_names_fullpath = []

		for source_file in source_file_names:
			source_file_names_fullpath.append(source_directory_fullpath + "/" + source_file)		
		for target_file in target_file_names:
			target_file_names_fullpath.append(target_directory_fullpath + "/" + target_file)

		# 获取目标合并目录下所有文件对应的MD5值数组
		md5_of_target_files = []

		for single_target_file_fullpath in target_file_names_fullpath:
			md5_of_target_files.append(calculate_MD5(single_target_file_fullpath))

		# 逐个比较源文件夹下文件的MD5值，是否在目标MD5数组中出现，出现则说明已存在相同文件，不出现则文件不同，文件拷贝到目标目录下，并更新MD5数组
		for single_source_file_fullpath in source_file_names_fullpath:

			current_md5 = calculate_MD5(single_source_file_fullpath)

			if not current_md5 in md5_of_target_files:
				# 	script_path = single_sudo_script_fullpath[0:single_sudo_script_fullpath.rfind("/")]
				script_name = single_source_file_fullpath.split("/")[-1]

				print color_yellow_start+"File: " + single_source_file_fullpath + " not in directory: " + target_directory_fullpath + ", begin copy."
				command = "cp "+single_source_file_fullpath+" "+target_directory_fullpath+"/"+script_name+time.strftime("_%Y_%m_%d_%H_%M_%S",time.localtime(time.time()))
				print "ececute command: "+command+color_end
				os.system(command)
			else:
				print color_green_start+"File: " + single_source_file_fullpath + " in directory: " + target_directory_fullpath + ", needn't to copy." + color_end


# 将所有host的sudo脚本merge到sudo数据库中
def merge_all_scprits_to_sudo_database():

	all_hosts_to_merge_abspath = get_all_hosts_scripts_dirname_to_merge_abspath()
	print "All scripts to merge of directory: \n",all_hosts_to_merge_abspath

	# 遍历每个host-scripts目录
	for host_scripts_dir in all_hosts_to_merge_abspath:

		# 对于host_scripts_dir中所有文件，如果在all_hosts_to_merge_abspath中不存在，则直接拷贝过去
		# todo 实现交互式询问加入 
		merge_two_directory_directly(host_scripts_dir, get_scriptDB_abs_path()) 


def main():

	merge_all_scprits_to_sudo_database()


if __name__ == '__main__':
	main()
