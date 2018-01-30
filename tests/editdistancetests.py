import random
import sys
import os
from fuzzywuzzy import fuzz

scr = open("shortscript.txt", "r")
sub = open("shortsub.txt", "r")

timingLine = "00:00:00,000 --> 00:00:00,000"

lines = []
lines2 = []



for line in scr:

    i = 0
    myList = list(line)
    while i < len(myList):
        if not myList[i].isalpha():
            if myList[i] == '(':
                while not myList[i] == ')' and not myList[i] == '\n':
                    myList[i] = ''
                    i = i+1
            elif myList[i] == ')':
                myList[i] = myList[i]
            else:
                myList[i] = ''

        i = i+1


    line = "".join(myList)
    if(line.isupper()):
        line = ">>>>>" + line
    else:
        line = line.lower()

    if len(lines) == 0:
        lines.append(">>>>>START")
        lines.append("")
        lines.append(line)
    elif lines[-1] == "" and not lines[-2].isupper() and not line.isupper():
        lines.append(">>>>>DESCRIPTION")
        lines.append("")
        lines.append(line)
    else:
        lines.append(line)



for line in sub:
    i = 0
    myList = list(line)

    line = "".join(myList)
    if not line == '':
        subs.append(line)



for i in lines:
    print(i)
for i in lines2:
    print(i)

scr.close()
sub.close()