import random
import sys
import os
from fuzzywuzzy import fuzz

scr = open("shortscript.txt", "r")
sub = open("shortsub.txt", "r")

timingLine = "00:00:00,000 --> 00:00:00,000"

pars = 0
fmtdScr = []
fmtdSubs = []

##
##formatting script file
##
for scrLine in scr:
    i = 0
    scrList = list(scrLine)

    while i < len(scrList):
        if not scrList[i].isAlpha():
        	if scrList[i] == '(':
        		pars = pars + 1
        	elif scrList == ')':
        		pars = pars - 1
        	else:
        		scrList[i] = ''
        else:
        	if pars > 0:
        		scrList = ''
        i = i+1

    scrLine = "".join(scrList)
    if(scrLine.isupper()):
        scrLine = ">>>>>" + scrLine
    else:
        scrLine = scrLine.lower()

    if len(fmtdScr) == 0:
        fmtdScr.append(">>>>>START")
        fmtdScr.append("")
        fmtdScr.append(scrLine)
    elif fmtdScr[-1] == "" and not fmtdScr[-2].isupper() and not scrLine.isupper():
        fmtdScr.append(">>>>>DESCRIPTION")
        fmtdScr.append("")
        fmtdScr.append(scrLine)
    else:
        fmtdScr.append(scrLine)

##
##formatting sub file
##
for line in sub:
    i = 0
    myList = list(line)

    line = "".join(myList)
    if not line == '':
        fmtdSubs.append(line)


##
##printing formatted files
##
for i in fmtdScr:
    print(i)
##for i in fmtdSubs:
##    print(i)

scr.close()
sub.close()