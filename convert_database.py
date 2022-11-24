import numpy as np
import os
import json

from flask import Flask, Response, request

import glob
import math
import random

from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

def VAE_clustering(embeds, cluster_threshold=0.7):
    num_clusters, clusters = sklearn.cluster_euclidean_dist(embeds)
    return num_clusters, clusters

def cluster_by_hand(embeddings, names, cluster_threshold=0.90):
    embeddings_copy = embeddings.copy()
    if type(embeddings_copy) != 'list':
        embeddings_copy = embeddings_copy.tolist()
    #embeddings_copy = list(embeddings.copy)
    names_copy = names.copy()
    print('Clustering embeddings with {} elements.'.format(len(embeddings)))
    clusters_names = []
    while len(embeddings_copy) > 2:
        print(len(embeddings_copy), ' left to process.')
        local_cluster = [0]
        try:
            similarities = cosine_similarity([embeddings_copy[0]], embeddings_copy[1:])
        except:
            print(len(embeddings_copy))
            break
        #print(similarities.shape)
        for i, similarity in enumerate(similarities[0]):
            if similarity > cluster_threshold:
                local_cluster.append(i + 1)
        
        clusters_names.append([names_copy[item] for item in local_cluster])
        
        counter = 0
        for index in local_cluster:
            del embeddings_copy[index - counter]
            del names_copy[index - counter]
            counter += 1
    
    if len(names_copy) == 1:
        clusters_names.append(names_copy)
    
    return clusters_names


model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

app = Flask(__name__)

@app.route('/process', methods=['GET', 'POST'])
def text_to_embedding():
	data = request.get_json()
	text = data['text']
	embedding = model.encode(text)
	result = {'embedding': embedding.tolist()}
	resp = Response(json.dumps(result), status=200, mimetype='application/json')
	return resp

@app.route('/compare', methods=['GET','POST'])
def compare():
	data = request.get_json()
	texts = data['text'].split('.')[:2]
	embedding_a = model.encode(texts[0])
	embedding_b = model.encode(texts[1])
	distance = cosine(embedding_a, embedding_b)
	result = {'distance': distance}
	resp = Response(json.dumps(result), status=200, mimetype='application/json')
	return resp


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='8000')