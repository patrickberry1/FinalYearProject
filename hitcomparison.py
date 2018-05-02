import json

with open("files/sw4_speech.json") as j_data:
    orgnl = json.load(j_data)

with open("sw4specific/files/sw4_speech.json") as json_data:
    new = json.load(json_data)

o_hit_count = 0
n_hit_count = 0
o_total = 0
n_total = 0

for item in orgnl['movie_script']:
    o_total += 1
    if item['start_time'] != '':
        o_hit_count += 1

for item in new['movie_script']:
    n_total += 1
    if item['start_time'] != '':
        n_hit_count += 1

o_hit_ratio = float(o_hit_count) / float(o_total)
n_hit_ratio = float(n_hit_count) / float(n_total)

print('original hit count was: ' + str(o_hit_count) + ", giving a hit ratio of: " + str(o_hit_count) + "/" + str(
    o_total) + "=" + str(o_hit_ratio))
print('new hit count was: ' + str(n_hit_count) + ", giving a hit ratio of: " + str(n_hit_count) + "/" + str(
    n_total) + "=" + str(n_hit_ratio))
