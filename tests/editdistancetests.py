import random
import sys
import os
from fuzzywuzzy import fuzz

scr = open("shortscript.txt", "r")
sub = open("shortsub.txt", "r")
subout = open("formatted_subs.txt", "w+")
scrout = open("formatted_scr.txt", "w+")

fmtdScr = []
fmtdSubs = []

##
##formatting script file
##
for scrLine in scr:

    i = 0
    scrList = list(scrLine)
    inSent = False
    inPars = False

    ##remove non-alphanumeric characters from lines in script
    ##and remove text within parentheses
    while i < len(scrList):
        if not scrList[i].isalnum():
        	if scrList[i] == '(':
        		inPars = True
        		scrList[i] = ''
        	elif scrList == ')':
        		inPars = False
        		scrList[i] = ''
        	elif scrList[i] == ' ' and inSent:
        		scrList[i] = scrList[i]
        	else:
        		scrList[i] = ''
        else:
        	inSent = True
        	if inPars:
        		scrList[i] = ''
        i = i+1

    ##converting list back into string and removing white space
    ##formatting headers
    scrLine = "".join(scrList)
    if(scrLine.isupper()):
        scrLine = ">>>>>" + scrLine
    else:
        scrLine = scrLine.lower()

    fslen = len(fmtdScr)

    ##adding tags and appending individual formatted lines together
    if fslen == 0:
        fmtdScr.append(">>>>>START")
        fmtdScr.append(scrLine)
    elif not fmtdScr[fslen-2].isupper() and fmtdScr[fslen-1] == "" and not scrLine.isupper():
    	fmtdScr.append(">>>>>DESC")
        fmtdScr.append(scrLine)
    else:
        fmtdScr.append(scrLine)

##
##formatting sub file
##
skip = 0
x = 1
timing = False
times = []
temp = ""

for l in sub:
	num = str(x) + '\n'
	if l == num:
		ind = 0
		temp = temp.lower()
		tempList = list(temp)
		while ind < len(tempList):
			if not tempList[ind].isalnum() and tempList[ind] != ' ':
				tempList[ind] = ''
			ind = ind + 1
		if len(tempList) > 0:
			fmtdSubs.append(''.join(tempList))
		x = x+1
		timing = True
		temp = ""
	elif timing:
		times.append(l)
		timing = False
	else:
		temp = temp + l


for line in times:
	line = line.split("-->")
	print(line)

##
##printing formatted files
##
for line in fmtdSubs:
    subout.write(line + '\n')
for line in fmtdScr:
	scrout.write(line + '\n')

scr.close()
sub.close()