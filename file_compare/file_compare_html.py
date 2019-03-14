# coding=utf-8

import difflib
import sys

output_file_name = "differences.html"

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
    output_content = d.make_file(file_content1,file_content2)

    with open(output_file_name,"w+") as fd:
        fd.write(output_content)


if __name__ == '__main__':
    main()