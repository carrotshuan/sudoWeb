# coding=utf-8

import difflib
import sys

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
except Exception as e:
    print "Arguments Error."

def readfile(filename):

    with open(filename) as fd:

        file_content = fd.read().splitlines()

    return file_content

def main():

    file_content1 = readfile(textfile1)
    file_content2 = readfile(textfile2)
    
    d = difflib.HtmlDiff()
    print(d.make_file(file_content1,file_content2))

if __name__ == '__main__':
    main()