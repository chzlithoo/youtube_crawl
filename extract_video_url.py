import csv

with open('meta_videos.csv', 'r', newline='', encoding='utf-8') as csv_file:
	lines = csv_file.readlines()
res = csv.reader(lines)
with open('video_urls.csv', 'w') as wr:
	out_writer = csv.writer(wr, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		out_writer.writerow([r[1], r[2]])

