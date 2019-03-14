# coding=utf-8

import difflib
import sys

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
except Exception as e:
    print "Arguments Error."

def main():

    file_content1 = open(textfile1).readlines()
    file_content2 = open(textfile2).readlines()
    
    # diff = difflib.ndiff(file_content1, file_content2)
    # diff = difflib.context_diff(file_content1, file_content2)

    diff = difflib.unified_diff(file_content1, file_content2) # 按GIT标准格式输出

    for line in diff:
        if not line.startswith(" "):
            print line,

if __name__ == '__main__':
    main()