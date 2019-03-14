# coding=utf-8

import threading
import os
import time

import sys
from select import select


timeout = 5
print "Enter something:",
rlist, _, _ = select([sys.stdin], [], [], timeout)


if rlist:
	
	
    s = sys.stdin.readline()
    print s
else:
    print "No input. Moving on..."