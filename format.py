import random, sys, os, argparse, json, re, urllib.request
from bs4 import BeautifulSoup, Tag, UnicodeDammit
from fuzzywuzzy import fuzz

# scr = open("shortscript.txt", "r")
sub = open("subtrack.txt", "r")
subout = open("formatted_subs.txt", "w+")
timeout = open("timings.txt", "w+")
# scrout = open("formatted_scr.txt", "w+")

# fmtdScr = []
formatted_subs = []
script_url = ''

##
##formatting script file
##
movie_name = input('Enter the name of the movie for the passed script.')
argparser = argparse.ArgumentParser(description=hello)
argparser.add_argument('script_url', metavar='script_url', type=str, nargs='?',
                       help='URL of the webpage containing the movie script')

args = argparser.parse_args()

if (args.script_url != None):
    script_url = args.script_url

request = urllib.request.Request(script_url)
webpage_bytes = urllib.request.urlopen(request)
soup = BeautifulSoup(webpage_bytes, 'lxml')

script_text = soup.find("pre")

if( script_text.find("pre") ):
    print('Found a <pre> inside the <pre>')
    script_text = script_text.find("pre")


script = dict()
script['movie_url'] = request.full_url

script['movie_title'] = input('Movie name:')

BLOCK_TYPES=['character', 'speech', 'stage direction', 'location']
CHARACTER=0
SPEECH=1
DIRECTIONS=2
LOCATION=3


spaces_regex = re.compile("^(\s*).*")
location_regex = re.compile("^\s*(INT\.|EXT\.)")


#
# ---------- Func for definging/determining text block types ----------
#
def get_line_type(line, stripped_line, usual_spaces, characters):
    # Counting the number of spaces at the beginning of the line
    spmatch = spaces_regex.search(line)
    spaces_number = len(spmatch.group(1))
    block_type = 0

    if( location_regex.search(line) != None ):
        return LOCATION

    if stripped_line in characters:
        return CHARACTER

    # Look for space
    for block_type_usual_spaces in usual_spaces:
        if spaces_number in block_type_usual_spaces:
            block_type = usual_spaces.index(block_type_usual_spaces)
            return usual_spaces.index(block_type_usual_spaces)

    print('There are {:d} spaces at the beginning of this line'.format(spaces_number))
    question = "What kind of block is this?\n"
    for i in range(len(BLOCK_TYPES)):
        question += '\t('+str(i)+') ' + BLOCK_TYPES[i] + '\n'
    print(question)

    validated = False
    while( validated == False):
        try:
            block_type = int(input('? [0-{:d}] '.format(len(BLOCK_TYPES)-1)))
            while( block_type < 0 or block_type >= len(BLOCK_TYPES)):
                block_type = int(input('? [0-{:d}] '.format(len(BLOCK_TYPES)-1)))
        except ValueError:
            continue

        validated = True

    remember_spaces = False
    validated = False
    while( validated == False):
        answer_spaces = input('Are all  lines with {:d} leading spaces \'{:s}\' blocks ? (Y/n) '.format(
                spaces_number, BLOCK_TYPES[block_type]))

        if( answer_spaces == 'n' or answer_spaces =='N' ):
            print('You said no: we will ask you again next time.')
            remember_spaces = False
        else:
            print('You said yes: ' +
                  'every new block with {:d} leading spaces '.format(spaces_number) +
                  'will now be considered a \'{:s}\'.'.format(BLOCK_TYPES[block_type]) )
            remember_spaces = True

        validated = True

    if( remember_spaces ):
        usual_spaces[block_type].append(spaces_number)

    return block_type



#
# ---------- Main loop for parsing script
#

usual_spaces=[[] for i in range(len(BLOCK_TYPES))]

is_intro = True
movie_script = []
intro = []
last_line_type = -1
last_character = ''
text = []
characters=[]

for block in script_text.descendants:
    # If block is an instance of bs4.Tag, its surrounded by HTML tags
    # The next block contains the same text without the tags
    # So we continue without parsing this block
    if(isinstance(block, Tag)):
        continue

    # UnicodeDammit converts string to UTF-8
    block = UnicodeDammit(block, soup.original_encoding).unicode_markup
    # remove leading and ending new line chars
    block = block.strip('\n')

    # if the block doesn't have any text, skip it
    if( re.search('\w', block) == None ):
        continue

    for line in block.split('\n'):
        stripped_line = line.strip(' \n\t\r')
        if( re.search('\w', line) == None ):
            continue

        print('                       ------- Begin line -------')
        print(line)
        print('                        ------- End line -------')

        if( is_intro ):
            print()
            answer = input("Still intro? (Y/n) ")

            if(answer == 'n' or answer == 'N'):
                is_intro = False
                movie_script.append({
                    'type': 'introduction',
                    'text': '\n'.join(intro)})
                print(movie_script[-1])
            else:
                intro.append(stripped_line)
                continue


        line_type = get_line_type(line, stripped_line, usual_spaces, characters)
        print("The last line was interpreted as '{}'".format(BLOCK_TYPES[line_type]))
        print()

        if(last_line_type == -1 # -1 = not initialized
           or last_line_type == line_type):
            text.append(stripped_line)
        else:
            if(last_line_type == CHARACTER):
                last_character='\n'.join(text)
                if not last_character in characters:
                    characters.append(last_character)
            elif(last_line_type == SPEECH):
                movie_script.append({
                    'type': BLOCK_TYPES[last_line_type],
                    BLOCK_TYPES[CHARACTER]: last_character,
                    'text': '\n'.join(text)})
                print('We just parsed this JSON block:')
                print(movie_script[-1])
            else:
                movie_script.append({
                    'type': BLOCK_TYPES[last_line_type],
                    'text': '\n'.join(text)})
                print('We just parsed this JSON block:')
                print(movie_script[-1])
            text=[stripped_line]

        last_line_type = line_type

        print()

    print()
    print()

movie_script.append({
    'type': BLOCK_TYPES[line_type],
    'text': '\n'.join(text)})


script['movie_script'] = movie_script

print('(Our current directory is: {})'.format(os.getcwd()), flush=True)
out_filename = input('output filename: ')

try:
    fd = open(out_filename, 'w+')
    json.dump(script, fd, indent=True)
    print('We just successfully wrote {}\'s script as JSON to {} .'.format(script['movie_title'], fd.name))
except:
    print("Shit happened: ", sys.exc_info()[0])
finally:
    fd.close()
    print()
    print('This script was made by Adrien Luxey for Pierre Peigné-Leroy in 2016.')
    print('It\'s free to use and all, go check our licence.')



#
# --------------------- formatting sub file ---------------------
#
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
        line_num = line_num + 1
        timing = True
        temp = ""
    elif timing:
        times.append(l)
        timing = False
    else:
        listl = list(l)
        len_listl = len(listl)
        if (listl[len_listl - 1] == "\n"):
            listl[len_listl - 1] = ' '
        new_l = ''.join(listl)
        temp = temp + new_l
formatted_subs.append(temp)

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

##
##printing formatted files
##
for line in new_times:
    timeout.write(line + '\n')
for line in formatted_subs:
    subout.write(line + '\n')

sub.close()
