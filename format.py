#!/usr/bin/python3
# coding: utf-8

import random, sys, os, argparse, json, re
from bs4 import BeautifulSoup, Tag, UnicodeDammit
from fuzzywuzzy import fuzz

#
#
# ------------------ formatting script file --------------------
#
#

# argparser= argparse.ArgumentParser(description='')
# argparser.add_argument('script_url', metavar='script_url', type=str, nargs='?',
#         help='URL of the webpage containing the movie script')

# args=argparser.parse_args()


# # loop until we get a valid script_url

# script_url = ''
# is_webpage_fetched = False
# while not is_webpage_fetched:
#     # get the script's URL from the parameters if it was passed
#     if( script_url == '' and args.script_url != None ):
#         script_url = args.script_url
#     else:
#         print('Enter an imsdb.com sript url:')

#         script_url = input('--> ')

#     try:
#         request = urllib.request.Request(script_url)
#         webpage_bytes = urllib.request.urlopen(request)
#         soup = BeautifulSoup(webpage_bytes, 'lxml')
#         print('Detected encoding is ', soup.original_encoding)
#         is_webpage_fetched = True
#     except urllib.error.URLError as err:
#         print('Caught a URLError while fetching URL:', err)
#         print()
#         pass
#     except ValueError as err:
#         print('Caught a ValueError while fetching URL:', err)
#         print()
#         pass
#     except:
#         print('Caught unrecognized error')
#         raise
#     else:
#         script_text = soup.find("pre")

#         # script text identified by pre tag in html
#         # checking for pre tag within first pre tag

#         if( script_text.find("pre") ):
#             script_text = script_text.find("pre")

#         is_webpage_fetched = True



# # script dict to be serialized as JSON
# script=dict()


# # Insert movie URL into dict
# script['movie_url'] = request.full_url

# # Insert movie name into dict
# answer = 'n'
# while (answer == 'n' or answer == 'N'):
#     script['movie_title'] = input("Enter movie title: ")


# BLOCK_TYPES=['character', 'speech', 'stage direction', 'location']
# CHARACTER=0
# SPEECH=1
# DIRECTIONS=2
# LOCATION=3


# # COMPILE ALL THE REGULAR EXPRESSIONS!
# spaces_regex = re.compile("^(\s*).*")
# location_regex = re.compile("^\s*(INT\.|EXT\.)")


# #
# # Function for determining and defining block types based on leading spaces
# #
# def get_line_type(line, stripped_line, usual_spaces, characters):
#     # Counting the number of spaces at the beginning of the line
#     spmatch = spaces_regex.search(line)
#     spaces_number = len(spmatch.group(1))
#     block_type = 0

#     if( location_regex.search(line) != None ):
#         return LOCATION

#     if stripped_line in characters:
#         return CHARACTER

#     # Look for space
#     for block_type_usual_spaces in usual_spaces:
#         if spaces_number in block_type_usual_spaces:
#             block_type = usual_spaces.index(block_type_usual_spaces)
#             return usual_spaces.index(block_type_usual_spaces)

#     print('There are {:d} space(s) at the beginning of this line'.format(spaces_number))
#     question = "What kind of block is this?\n"
#     for i in range(len(BLOCK_TYPES)):
#         question += '\t('+str(i)+') ' + BLOCK_TYPES[i] + '\n'
#     print(question)

#     validated = False
#     while(validated == False):
#         try:
#             block_type = int(input('? [0-{:d}] '.format(len(BLOCK_TYPES)-1)))
#             while( block_type < 0 or block_type >= len(BLOCK_TYPES)):
#                 block_type = int(input('? [0-{:d}] '.format(len(BLOCK_TYPES)-1)))
#         except ValueError:
#             continue

#         validated = True
#         answer = input('You said the last block type was \'{:s}\', sure about that? (Y/n) '.format(
#                 BLOCK_TYPES[block_type]))
#         if( answer == 'n' or answer =='N' ):
#             validated = False

#     remember_spaces = False
#     validated = False
#     while( validated == False):
#         answer_spaces = input('Are all  lines with {:d} leading spaces \'{:s}\' blocks ? (Y/n) '.format(
#                 spaces_number, BLOCK_TYPES[block_type]))

#         if( answer_spaces == 'n' or answer_spaces =='N' ):
#             print('You said no: we will ask you again next time.')
#             remember_spaces = False
#         else:
#             print('You said yes: ' +
#                   'every new block with {:d} leading spaces '.format(spaces_number) +
#                   'will now be considered a \'{:s}\'.'.format(BLOCK_TYPES[block_type]) )
#             remember_spaces = True

#         validated = True
#         answer = input('Are you sure? (Y/n) ')
#         if( answer == 'n' or answer =='N' ):
#             validated = False

#     if( remember_spaces ):
#         usual_spaces[block_type].append(spaces_number)

#     return block_type


# # Main formatting loop

# usual_spaces=[[] for i in range(len(BLOCK_TYPES))]

# is_intro = True
# movie_script = []
# intro = []
# last_line_type = -1
# last_character = ''
# text = []
# characters=[]


# print("Start by telling me when the introduction will end.")

# for block in script_text.descendants:
#     # if a block is an instance of bs4.Tag it's surrounded by HTML tags.
#     # the next block will be the same text without the tags so we continue without parsing this block
#     if(isinstance(block, Tag)):
#         continue

#     #converts string to utf-8
#     block = UnicodeDammit(block, soup.original_encoding).unicode_markup
#     # remove leading and ending new line chars
#     block = block.strip('\n')

#     # skip empty blocks of text
#     if( re.search('\w', block) == None ):
#         continue

#     for line in block.split('\n'):
#         stripped_line = line.strip(' \n\t\r')
#         if( re.search('\w', line) == None ):
#             continue
#         print()
#         print()
#         print('------------------------------ Begin line ------------------------------')
#         print(line)
#         print('                        ------- End line -------')
#         print()
#         print()

#         if( is_intro ):
#             print()
#             answer = input("Is this still part of the intro? (Y/n) ")

#             if(answer == 'n' or answer == 'N'):
#                 is_intro = False
#                 movie_script.append({
#                     'type': 'introduction',
#                     'text': '\n'.join(intro)})
#             else:
#                 intro.append(stripped_line)
#                 continue


#         line_type = get_line_type(line, stripped_line, usual_spaces, characters)
#         print("The last line was interpreted as '{}'".format(BLOCK_TYPES[line_type]))
#         print()

#         if(last_line_type == -1 # -1 = not initialized
#            or last_line_type == line_type):
#             text.append(stripped_line)
#         else:
#             if(last_line_type == CHARACTER):
#                 last_character='\n'.join(text)
#                 if not last_character in characters:
#                     characters.append(last_character)
#             elif(last_line_type == SPEECH):
#                 movie_script.append({
#                     'type': BLOCK_TYPES[last_line_type],
#                     BLOCK_TYPES[CHARACTER]: last_character,
#                     'text': '\n'.join(text)})
#                 print('We just parsed this JSON block:')
#                 print(movie_script[-1])
#             else:
#                 movie_script.append({
#                     'type': BLOCK_TYPES[last_line_type],
#                     'text': '\n'.join(text)})
#                 print('We just parsed this JSON block:')
#                 print(movie_script[-1])
#             text=[stripped_line]

#         last_line_type = line_type
#         print()

#     print()
#     print()

# movie_script.append({
#     'type': BLOCK_TYPES[line_type],
#     'text': '\n'.join(text)})

# print('We just parsed this JSON block:')
# print(movie_script[-1])
# print()
# print()

# script['movie_script'] = movie_script

# print('All done!')


# print(flush=True)
# print(flush=True)
# print('(Our current directory is: {})'.format(os.getcwd()), flush=True)
# out_filename = input('Enter output filename: ')

# try:
#     fd = open(out_filename, 'w')
#     json.dump(script, fd, indent=True)
#     print('Bravo!')
# except:
#     print("Shit broke: ", sys.exc_info()[0])
# finally:
#     fd.close()





#
#
# --------------------- formatting sub file ---------------------
#
#

print('formatting sub file')
line_num = 1
timing = False
times = []
temp = ""
sub = open("inputs/sw4_sub.txt", "r")
subout = open("outputs/sw4_fs.txt", "w+")
timeout = open("outputs/sw4_timings.txt", "w+")
formatted_subs = []

for l in sub:
    print(l)
    num = str(line_num)

    # stripping line of all characters that could mess up string comparisons
    # i.e. all non alphanumeric characters
    x = list(l)
    y = []
    for c in x:
    	if not c.isalnum() and c != ' ':
    		y.append('')
    	else:
    		y.append(c)
    x = ''.join(y)

    if x == num:
        if len(temp) > 0:
            temp_list = list(temp)
            char_index = 0

            # cleaning up line
            while char_index < len(temp_list):
                if not temp_list[char_index].isalnum() and temp_list[char_index] != ' ':
                    temp_list[char_index] = ''
                char_index = char_index + 1
            temp = ''.join(temp_list)
            temp = temp.lower()
            temp = temp.strip('\n\t\r')
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
        len_listl = len(listl)
        if (listl[len_listl - 1] == "\n"):
            listl[len_listl - 1] = ' '
        new_l = ''.join(listl)
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

# ---------- writing formatted files ----------
for line in new_times:
    timeout.write(line + '\n')
for line in formatted_subs:
    subout.write(line + '\n')

sub.close()
