import random
import sys
import os
import editdistance
from fuzzywuzzy import fuzz

# scr = open("sw4script.txt", "r")
# sub = open("subtrack.txt", "r")
#
# lines = []
# lineType = []
# prevLine = ''
#
#
# for line in scr:
#     print(str(editdistance.eval(line, prevLine)))
#     prevLine = line

line1 = 'Tear this ship apart and bring me the passengers, I want them alive'
line2 = 'Trooper, tear this ship apart and bring me the ambassador, I want her alive'

line3 = 'Goodbye pal'
line4 = 'Hello Luke'

fuzz = fuzz.ratio(line3, line4)

ed = editdistance.eval(line3, line4)
print(str(ed))
print(str(fuzz))
# scr.close()
# sub.close()