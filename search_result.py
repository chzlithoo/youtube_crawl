# -*- coding: utf-8 -*-
import csv
import json
import urllib.parse as url_prs
import urllib.request as url_req
from datetime import datetime

from bs4 import BeautifulSoup

youtube_search_url = "https://www.youtube.com/results?search_query="

search_query = url_prs.quote("난민 수용")
max_num_result = 20
count = 0
schema = [
	'publish_date', 'video_id', 'video_url',
	'title', 'channel_url', 'channel_name',
	'genre', 'short_description', 'full_description',
	'like', 'dislike', 'interaction_cnt']

with open('meta_videos.csv', 'w', newline='', encoding='utf-8') as csv_file:
	out_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	out_writer.writerow([g for g in schema])
	for search_page in range(1, 51):

		print("search page number:", search_page)

		video_url = youtube_search_url + search_query + '&page=' + str(search_page)
		search_result = url_req.urlopen(video_url)

		soup = BeautifulSoup(search_result, 'html.parser')
		result_item = soup.findAll('ol', {"class": "item-section"})
		result_content = soup.findAll('div', {"class": "yt-lockup-content"})

		if max_num_result > len(result_content):
			max_num_result = len(result_content)
			print("only %d search result(s) in page %d:" % (max_num_result, search_page))
		if max_num_result == 0:
			break

		for content in result_content:
			try:
				short_description = content.findAll('div', {"class": "yt-lockup-description"})[0].text
			except IndexError:
				print(content.findAll('div', {"class": "yt-lockup-description"}))
				short_description = ""
			title_link = content.findAll('a', {"class": "yt-uix-tile-link"})[0]
			title = title_link['title']
			video_link = title_link['href']
			if not video_link.startswith("/watch") or "&list=" in video_link:
				continue
			video_url = 'https://www.youtube.com' + video_link
			video_id = video_link.split("v=")[1]
			video_response = url_req.urlopen(video_url)
			video_content_html = BeautifulSoup(video_response, 'html.parser')
			publish_date = video_content_html.find_all('meta', {"itemprop": "datePublished"})[0]["content"]
			converted_date = datetime.strptime(publish_date, "%Y-%m-%d")
			
			if datetime(2018, 6, 1) >= converted_date or converted_date > datetime(2019, 1, 1):
				continue
			full_description = ''
			for p in video_content_html.find_all('p', id='eow-description'):
				full_description += p.get_text('\n')
			# comment_count=video_content_html.find_all("h2", {"class":"style-scope ytd-comments-header-renderer"})[0].text
			try:
				like = video_content_html.find_all('button', {"class": "like-button-renderer-like-button"})[0].span.text
			except AttributeError:
				like = 0
			try:
				dislike = video_content_html.find_all('button', {"class": "like-button-renderer-dislike-button"})[
					0].span.text
			except AttributeError:
				dislike = 0

			genre = video_content_html.find_all('meta', {"itemprop": "genre"})[0]["content"]
			interaction_cnt = video_content_html.find_all('meta', {"itemprop": "interactionCount"})[0]["content"]

			channel_json_str = video_content_html.findAll('script', type='application/ld+json')[0].text
			channel_json = json.loads(channel_json_str)['itemListElement'][0]['item']

			channel_url = channel_json['@id']
			channel_name = channel_json['name']

			result_string = [
				publish_date, video_id, video_url,
				title, channel_url, channel_name,
				genre, short_description, full_description,
				like, dislike, interaction_cnt]
			out_writer.writerow(result_string)
			count += 1
			if count % 10 == 0:
				print("saved %s lines" % count)
