#!/usr/bin/python3

import sys

sys.stdout.flush()
data = sys.stdin.readlines()
string = data[0][:-1]
string = string.split('///')

for i in string:
    print(i)

