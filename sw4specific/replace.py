import json

with open("../files/sw4_script.json") as json_data:
	scr = json.load(json_data)

with open("../files/sw4_speech.json") as json_data:
	sp = json.load(json_data)


for item in scr['movie_script']:
	t = item['text']
	t = t.replace('artoo', 'r2')
	t = t.replace('detoo', 'd2')
	t = t.replace('Artoo', 'r2')
	t = t.replace('Detoo', 'd2')
	item['text'] = t


for item in sp['movie_script']:
	t = item['text']
	t = t.replace('artoo', 'r2')
	t = t.replace('detoo', 'd2')
	t = t.replace('Artoo', 'r2')
	t = t.replace('Detoo', 'd2')
	item['text'] = t


nscr = open("files/new_sw4_scr.json", "w+")
nsp = open("files/new_sw4_sp.json", "w+")

nscr.write(json.dumps(scr, indent=2))
nsp.write(json.dumps(sp, indent=2))