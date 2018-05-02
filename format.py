#!/usr/bin/python3
# coding: utf-8

import random, sys, os, argparse, json, re
# from bs4 import BeautifulSoup, Tag, UnicodeDammit
from fuzzywuzzy import fuzz


#
#
# --------------------- formatting sub file ---------------------
#
#

# print('formatting sub file')
line_num = 1
timing = False
times = []
temp = ""
sub = open("files/sw4_sub.txt", "r")
subout = open("files/sw4_fs.txt", "w+")
timeout = open("files/sw4_timings.txt", "w+")
formatted_subs = []

for l in sub:
    # print(l)
    num = str(line_num)
    x = l.lower()
    x = l.strip('\n\t\r')
    if x == num:
        if len(temp) > 0:
            formatted_subs.append(temp)
        line_num = line_num + 1
        timing = True
        temp = ""

    # separating times from subtitles for easier parsing
    elif timing:
        times.append(l)
        timing = False
    # app
    else:
        listl = list(l)
        len_listl = len(listl)-1

        # cleaning up line
        while len_listl >= 0:
            if len_listl == 0 and listl[len_listl] == '-':
                # print('this worked')
                listl[len_listl] = '-'
            elif not listl[len_listl].isalnum() and listl[len_listl] != ' ':
                listl[len_listl] = ''
            len_listl = len_listl - 1
        new_l = ''.join(listl)
        new_l = new_l.lower()
        new_l = new_l.strip('\n\t\r')
        temp = temp + new_l

# Appending final line as for loop appends when it reaches next index line
formatted_subs.append(temp)

# Cleaning up times: removing new line chars
new_times = []
for line in times:
    line_array = list(line)
    ll = len(line_array)
    if line_array[ll - 1] == "\n":
        line_array[ll - 1] = ''
    elif line_array[0] == "\n":
        line_array[0] = ''
    new_line = ''.join(line_array)
    new_times.append(new_line)

# passing trhough a second time to account for lines which need to be split into multiple lines

l = len(formatted_subs)
i = 0
new_fs = []
new_t = []

while i < l:
    if '-' not in formatted_subs[i]:
        new_fs.append(formatted_subs[i])
        new_t.append(new_times[i])
    else:
        item = formatted_subs[i]
        item_list = item.split('-')
        new_fs.append(item_list[1])
        new_fs.append(item_list[2])
        new_t.append(new_times[i])
        new_t.append(new_times[i])
    i += 1

# ---------- writing formatted files ----------
for line in new_t:
    timeout.write(line + '\n')
for line in new_fs:
    subout.write(line + '\n')

sub.close()
