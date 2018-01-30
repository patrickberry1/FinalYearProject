import random
import sys
import os
import editdistance

scr = open("sw4script.txt", "r")
sub = open("subtrack.txt", "r")

lines = []
lineType = []


for line in scr:
    '''
    l = line
    for line in sub:
        if editdistance.eval(line, l) < 30:
            lines.append(l)
    '''
    s = ""
    for c in scr:
        if c.isupper():
            s = s + c
    print(s)

print(lines)

scr.close()
sub.close()