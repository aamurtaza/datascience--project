#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
from time import time

import pandas as pd
import os
import string
import nltk
from nltk.corpus import stopwords


def make_document(reviews):
    passage = ""
    for review in reviews:
        passage = passage + review + "\n"
    return passage

def make_corpus(hotels):
    corpus = []
    for hotel_name in hotels:
        hotel = hotels_data[hotels_data['name'] == hotel_name]
        hotel["combine_reviews"] = hotel['review_title'].map(str) +" "+ hotel['review'].map(str)
        document = make_document(hotel["combine_reviews"])
        document = document + hotel['tags'].iloc[0]
        corpus.append(document)
    return corpus
    
base_path =  os.path.dirname(os.path.abspath('__file__'))   

### ------------------------- Load files
hotels_data = pd.read_csv(base_path + "/datasets/Finland_Hotels_Reviews.csv")

### ------------------------- Preprocessing on textual data (review_title, reviews and tags)

# Removing all digits, stopwords as well as punctuation
stop = stopwords.words('english') + list(string.punctuation)

hotels_data['review_title'] = hotels_data['review_title'].astype(str).str.replace('\d+', '')
hotels_data['review'] = hotels_data['review'].astype(str).str.replace('\d+', '')
hotels_data['tags'] = hotels_data['tags'].astype(str).str.replace(':', ' ')
hotels_data['tags'] = hotels_data['tags'].astype(str).str.replace('\d+', '')

hotels_data['review_title'] = hotels_data['review_title'].apply(lambda words:' '.join([word for word in words.split() if word not in (stop)]))
hotels_data['review'] = hotels_data['review'].apply(lambda words:' '.join([word for word in words.split() if word not in (stop)]))
hotels_data['tags'] = hotels_data['tags'].apply(lambda words:' '.join([word for word in words.split() if word not in (stop)]))

# Applying stemming
stemmer = nltk.stem.SnowballStemmer('english')
hotels_data['review_title'] = hotels_data['review_title'].apply(lambda words: ' '.join([stemmer.stem(word) for word in words.split()]))
hotels_data['review'] = hotels_data['review'].apply(lambda words: ' '.join([stemmer.stem(word) for word in words.split()]))
hotels_data['tags'] = hotels_data['tags'].apply(lambda words: ' '.join([stemmer.stem(word) for word in words.split()]))

# Make corpus of hotel documents. Document is made using hotels review_title, review and tags
hotels = hotels_data['name'].unique()
corpus = make_corpus(hotels)

### ------------------------- Apply Clustering
vectorizer = TfidfVectorizer(analyzer='word', max_df=0.5, min_df = 2, stop_words = 'english', norm='l2', binary=False)
tfidf_matrix = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names()
rows, columns = tfidf_matrix.shape

n_cluster = 5
km = KMeans(n_clusters=n_cluster, init='k-means++', max_iter=100, n_init=1)
print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(tfidf_matrix)
print("done in %0.3fs" % (time() - t0))
print()
print("done in %0.3fs" % (time() - t0))
print()

print("Homogeneity: %0.3f" % metrics.homogeneity_score(hotels, km.labels_))
print("Completeness: %0.3f" % metrics.completeness_score(hotels, km.labels_))
print("V-measure: %0.3f" % metrics.v_measure_score(hotels, km.labels_))
print("Adjusted Rand-Index: %.3f"
      % metrics.adjusted_rand_score(hotels, km.labels_))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(tfidf_matrix, km.labels_, sample_size=1000))
print()

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
file = open(os.path.expanduser(r""+base_path+"/models/cluster_model.txt"), "wb")
for i in range(0,n_cluster):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :100]:
        print(' %s' % terms[ind], end='')
        record = str(terms[ind]) + " "
        file.write(bytes(record, encoding="ascii", errors='ignore'))
    file.write(bytes("\n,\n", encoding="ascii", errors='ignore'))
    print()
file.close()