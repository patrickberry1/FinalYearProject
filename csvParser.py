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