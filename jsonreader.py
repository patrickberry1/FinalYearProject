import json
from pprint import pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#opening files
timings = open("files/sw4_timings.txt", "r")
subs = open("files/sw4_fs.txt", "r")
new_json1 = open("files/sw4_speech.json", "w+")
new_json2 = open("files/sw4_script.json", "w+")
with open("files/sw4_parsed_script.json") as json_data:
	d = json.load(json_data)

with open("files/sw4_parsed_script.json") as json_data:
	new_d = json.load(json_data)

sub_list = []

for line in subs:
	sub_list.append(line)	

# splitting times into start and end times
timing_list = []
for line in timings:
	split_time = line.split('-->')
	timing_list.append(split_time)

#
# ---------- fuzzy string comparison ----------
#
sub_index = 0
sub_len = len(sub_list)
time_len = len(timing_list)
start_time = ''
end_time = ''
sub_text = ''

# for j in d['movie_script']:
# 	scr_text = j['text']
# 	start_index = sub_index
# 	curr_ratio = 1
# 	prev_ratio = 0
# 	sub_text = ""

# 	while curr_ratio > prev_ratio and sub_index < sub_len:
# 		sub_text = sub_text + sub_list[sub_index]
# 		prev_ratio = curr_ratio
# 		curr_ratio = fuzz.ratio(sub_text, scr_text)
# 		sub_index = sub_index + 1
	
# 	sub_index = sub_index - 1
# 	j['start_time'] = timing_list[start_index][0]
# 	j['end_time'] = timing_list[sub_index-1][1]


for j in d['movie_script']:
	if j['type'] == 'speech':
		j['start_time'] = ''
		j['end_time'] = ''
		scr_text = j['text']
		start_index = sub_index
		curr_ratio = 1
		prev_ratio = 0
		sub_text = ""
		temp_sub_index = sub_index + 1

		while curr_ratio > prev_ratio and sub_index < sub_len:
			sub_text = sub_text + sub_list[sub_index]
			prev_ratio = curr_ratio
			curr_ratio = fuzz.ratio(sub_text, scr_text)
			sub_index = sub_index + 1

		if curr_ratio < 50 and prev_ratio < 50:
			sub_index = temp_sub_index
		else:
			sub_index = sub_index - 1
			st = timing_list[start_index][0]
			st = st.replace(' ', '')
			j['start_time'] = st
			if sub_index == sub_len -1:
				et = timing_list[sub_index][1]
				et = et.replace("\n", "")
				et = et.replace(" ", "")
				j['end_time'] = et
			else:
				et = timing_list[sub_index-1][1]
				et = et.replace('\n', '')
				et = et.replace(' ', '')
				j['end_time'] = et

# dropping all stage direction, locations etc. from json file for time being
new_script = []

for i in d['movie_script']:
	if i['type'] == 'speech':
		temp_text = i['text']
		tt_list = list(temp_text)
		tt_index = 0
		while tt_index < len(tt_list):
			if tt_list[tt_index] == '\n':
				tt_list[tt_index] = ' '
			elif not tt_list[tt_index].isalnum() and tt_list[tt_index] != ' ':
				tt_list[tt_index] = ''
			tt_index = tt_index + 1
		temp_text = ''.join(tt_list)
		i['text'] = temp_text.lower()
		new_script.append(i)

new_d['movie_script'] = new_script

# sample_text = d['movie_script'][0]['text']
# sample_sub = ''
# while sub_index < 10:
# 	sample_sub = sample_sub + sub_list[sub_index]
# 	pprint(fuzz.ratio(sample_text, sample_sub))
# 	sub_index = sub_index + 1

new_json1.write(json.dumps(new_d, indent=2))
new_json2.write(json.dumps(d, indent=2))		























