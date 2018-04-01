import random
import sys
import os
from fuzzywuzzy import fuzz

# scr = open("shortscript.txt", "r")
sub = open("subtrack.txt", "r")
subout = open("formatted_subs.txt", "w+")
timeout = open("timings.txt", "w+")
# scrout = open("formatted_scr.txt", "w+")

# fmtdScr = []
formatted_subs = []

# ##
# ##formatting script file
# ##
# for scrLine in scr:

#     i = 0
#     scrList = list(scrLine)
#     inSent = False
#     inPars = False

#     ##remove non-alphanumeric characters from lines in script
#     ##and remove text within parentheses
#     while i < len(scrList):
#         if not scrList[i].isalnum():
#         	if scrList[i] == '(':
#         		inPars = True
#         		scrList[i] = ''
#         	elif scrList == ')':
#         		inPars = False
#         		scrList[i] = ''
#         	elif scrList[i] == ' ' and inSent:
#         		scrList[i] = scrList[i]
#         	else:
#         		scrList[i] = ''
#         else:
#         	inSent = True
#         	if inPars:
#         		scrList[i] = ''
#         i = i+1

#     ##converting list back into string and removing white space
#     ##formatting headers
#     scrLine = "".join(scrList)
#     if(scrLine.isupper()):
#         scrLine = ">>>>>" + scrLine
#     else:
#         scrLine = scrLine.lower()

#     fslen = len(fmtdScr)

#     ##adding tags and appending individual formatted lines together
#     if fslen == 0:
#         fmtdScr.append(">>>>>START")
#         fmtdScr.append(scrLine)
#     elif not fmtdScr[fslen-2].isupper() and fmtdScr[fslen-1] == "" and not scrLine.isupper():
#     	fmtdScr.append(">>>>>DESC")
#         fmtdScr.append(scrLine)
#     else:
#         fmtdScr.append(scrLine)

##
##formatting sub file
##
line_num = 1
timing = False
times = []
temp = ""

for l in sub:
	num = str(line_num) + '\n'
	if l == num:
		if len(temp) > 0:
			temp_list = list(temp)
			char_index = 0
			while char_index < len(temp_list):
				if temp_list[char_index] == '\n':
					temp_list[char_index] = ' '
				elif not temp_list[char_index].isalnum() and temp_list[char_index] != ' ':
					temp_list[char_index] = ''
				char_index = char_index + 1
			temp = ''.join(temp_list)
			temp = temp.lower()
			formatted_subs.append(temp)
		line_num = line_num+1
		timing = True
		temp = ""
	elif timing:
		times.append(l)
		timing = False
	else:
		listl = list(l)
		len_listl = len(listl)
		if(listl[len_listl-1] == "\n"):
			listl[len_listl-1] = ' '
		new_l = ''.join(listl)
		temp = temp + new_l
formatted_subs.append(temp)

new_times = []
for line in times:
	line_array = list(line)
	ll = len(line_array)
	if line_array[ll-1] == "\n":
		line_array[ll-1] = ''
	elif line_array[0] == "\n":
		line_array[0] = ''
	new_line = ''.join(line_array)
	new_times.append(new_line)

##
##printing formatted files
##
for line in new_times:
	timeout.write(line + '\n')
for line in formatted_subs:
    subout.write(line + '\n')
# for line in fmtdScr:
	# scrout.write(line + '\n')

# scr.close()
sub.close()
