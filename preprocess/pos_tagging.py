from konlpy.tag import Kkma
import pandas as pd
import os

kkma = Kkma()


def meta_parse():
	meta_path = '../meta_videos.csv'
	meta_data = pd.read_csv(meta_path, error_bad_lines=False)
	title = meta_data[['title']]
	description = meta_data[['full_description']]
	return title, description


def preprocess(text):
	res = []
	pos_tagged = kkma.pos(text)
	for word in pos_tagged:
		if len(word) > 1 and word[1][0] in ["V", "M", "N"]:
			res.append(word[0])
	return ' '.join(res)


def main():
	comment_path = '../comments/'
	for cp in os.listdir(comment_path):
		comment_file_path = comment_path + cp
		video_id = cp.split(".csv")[0]
		data = pd.read_csv(comment_file_path)
		processed_docs = data['text'].map(preprocess)
		processed_docs.to_csv('../c/%s.csv' % video_id, index=False)
		# ex_path = 'comments/diRM3LHsc14.csv'
		# data = pd.read_csv(ex_path)


if __name__ == '__main__':
	main()
