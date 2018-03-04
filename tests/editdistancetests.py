import random
import sys
import os
from fuzzywuzzy import fuzz

scr = open("shortscript.txt", "r")
sub = open("shortsub.txt", "r")

timingLine = "00:00:00,000 --> 00:00:00,000"

frmtdScr = []
frmtdSbs = []
timings = []

parCount = 0;           '''Count to keep track of parentheses so can avoid writing instructions'''
cntDwn = 2;             '''Count to track when the end of a block of subtitles if finished'''


'''formatting the script file'''
for line in scr:
    i = 0
    scrList = list(line)
    while i < len(scrList):
        if not scrList[i].isalpha():
            if scrList[i] == '(':
                parCount += 1;
                scrList[i] = ''
            elif scrList[i] == ')':
                parCount -= 1;
            else:
                scrList[i] = ''
        if parCount > 0:
            scrList[i] = '';
        i = i+1

    line = "".join(scrList)
    if(line.isupper()):
        line = ">>>>>" + line
    else:
        line = line.lower()

    if len(frmtdScr) == 0:
        frmtdScr.append(">>>>>START")
        frmtdScr.append("")
        frmtdScr.append(line)
    elif frmtdScr[-1] == "" and not frmtdScr[-2].isupper() and not line.isupper():
        frmtdScr.append(">>>>>DESCRIPTION")
        frmtdScr.append("")
        frmtdScr.append(line)
    else:
        frmtdScr.append(line)

'''formatting the sub file'''
apnd = '';

for line in sub:
    if len(line) == 1:
        cntDwn = 2
        if apnd != '':
            frmtdSbs.append(apnd)
            frmtdSbs.append('')
        apnd = ''
    elif cntDwn == 0:
        apnd = apnd + line
    else:
        cntDwn = cntDwn - 1

for line in frmtdSbs:
    print(line)

scr.close()
sub.close()