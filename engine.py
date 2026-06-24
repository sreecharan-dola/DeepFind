import numpy as np
import pickle as pk
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity_score(vector_a, vector_b):
    score = (vector_a @ vector_b)/ (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
    return score


def sentence_similarity(files, query):
    #It creates the structure in data.pk
    #store = {'all_files': {},
     #        'query' : '',
      #       'query_vector' : None,
       #      'file_vectors' : []} #holds ('vector','score','filename', 'chunk')

    #with open('data.pk', 'wb') as fobj:
     #   pk.dump(store, fobj)

    with open('data.pk', 'rb') as fobj:
        data = pk.load(fobj)


    query_changed = data['query'] != query
    if query_changed:
        data['query'] = query
        data['query_vector'] = model.encode(query)
    query_vector = data['query_vector']

    #same_files = all(x in files for x in data['all_files'])
    same_files = (set(data['all_files']) == set(files))

    if not same_files:
        data['all_files'] = files
        data['file_vectors'] = []

        for file in files:
            with open(file) as fobj:
                all_text = fobj.read()
                words = all_text.split()
                for i in range(0, len(words), 80):
                    chunk = ' '.join(words[i: i+80])
                    chunk_vector = model.encode(chunk)
                    data['file_vectors'].append(
                        (chunk_vector, similarity_score(query_vector, chunk_vector), file, chunk))

    elif same_files and query_changed:
        for i in range(len(data['file_vectors'])):
            vector, score, file, chunk = data['file_vectors'][i]
            data['file_vectors'][i] = (vector, similarity_score(query_vector, vector), file, chunk)

    with open('data.pk', 'wb') as obj:
        pk.dump(data, obj)

    #sorted based on score
    sorted_file_vector = sorted(data['file_vectors'], key=lambda x: x[1], reverse=True)

    #index 0 = vector, index 1 = score, index 2 = filename, index 3 = chunk
    #top 3 chunks with high score
    top_picks = [(chunk,file_name,score) for _,score,file_name,chunk in sorted_file_vector[:3]]

    return top_picks

#top = sentence_similarity(files = {'sample.txt', 'sample2.txt'}, query = 'AI development Researchers continue exploring safer and more efficient machine learning techniques' )


