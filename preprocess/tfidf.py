# -*- coding: utf-8 -*-
from collections import Counter
import pandas as pd
import os
import csv
import gensim
import io
from gensim import models

processed_path = '../processed/'
data = {}


for pp in os.listdir(processed_path):
	ppath = processed_path+pp
	# data = data.append(pd.read_pickle(ppath))
	doc = list(pd.read_pickle(ppath))
	with io.open('../c/%s' % pp, 'w', encoding='utf8') as fp:
		w = csv.writer(fp,delimiter='\t')
		for comment in doc:
			# line = "\t".join(comment)
			#print(line)
			#out.write(line)
			w.writerow(comment)

#tfidf = models.TfidfModel(corpus)
#corpus_tfidf = tfidf[corpus]