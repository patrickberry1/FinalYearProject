import json, csv
from pprint import pprint

#opening files
location_data = open("files/sw4_location_data.csv", "w+")
csv_writer = csv.writer(location_data)
with open("files/sw4_script.json") as json_data:
	d = json.load(json_data)
lines = []
lines.append(['character', 'text', 'start_time', 'end_time', 'location', 'time in ms'])

for item in d['movie_script']:
	if item['type'] == 'location':
		loc_arr = item['text'].split('-')
		temp = loc_arr[0]
		temp = temp.strip('EXT.')
		temp = temp.strip('INT.')
		curr_location = temp
		temp_arr = loc_arr[1:]
		sub_loc = ''.join(temp_arr)
	elif item['type'] == 'speech' and item['start_time'] != '':
		start_time = item['start_time']
		end_time = item['end_time']

		st_arr = start_time.split(':')
		et_arr = end_time.split(':')
		temp_st = st_arr[2].split(',')
		temp_et = et_arr[2].split(',')

		time_in_ms = ((int(et_arr[0])*60*60*1000) + (int(et_arr[1])*60*1000) + (int(temp_et[0])*1000) + int(temp_et[1])) - ((int(st_arr[0])*60*60*1000) + (int(st_arr[1])*60*1000) + (int(temp_st[0])*1000) + int(temp_st[1]))

		line = [item['character'], item['text'], item['start_time'], item['end_time'], curr_location, str(time_in_ms)]
		lines.append(line)

csv_writer.writerows(lines)