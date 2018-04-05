import json
from pprint import pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#opening files
timings = open("outputs/sw4_timings.txt", "r")
subs = open("outputs/sw4_fs.txt", "r")
new_json = open("outputs/sw4_json.json", "w+")
with open("inputs/sw4_parsed_script.json") as json_data:
	d = json.load(json_data)

sub_list = []

for line in subs:
	sub_list.append(line)	

# splitting times into start and end times
timing_list = []
for line in timings:
	split_time = line.split('-->')
	timing_list.append(split_time)



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
		i['start_time'] = ''
		i['end_time'] = ''
		new_script.append(i)

d['movie_script'] = new_script

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
		j['start_time'] = timing_list[start_index][0]
		if sub_index == sub_len -1:
			j['end_time'] = timing_list[sub_index][1]
		else:
			j['end_time'] = timing_list[sub_index-1][1]

# sample_text = d['movie_script'][0]['text']
# sample_sub = ''
# while sub_index < 10:
# 	sample_sub = sample_sub + sub_list[sub_index]
# 	pprint(fuzz.ratio(sample_text, sample_sub))
# 	sub_index = sub_index + 1

new_json.write(json.dumps(d, indent=2))
		

pprint(d)























