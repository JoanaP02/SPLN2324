from gensim.models import TfidfModel, Word2Vec, Doc2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from gensim.utils import tokenize
import nltk 
import ijson
import numpy as np
import tensorflow_hub as hub

def read_json_file(filename):
    with open(filename, 'r') as file:
        json_data = file.read()
    return json_data

def extract_items(json_data):
    extracted_data = {}
    for item in ijson.items(json_data, 'item'):
        extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

def preprocess(line):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

# Ler o arquivo JSON
filename = "DRE_small.json"
json_data = read_json_file(filename)

# Extrair dados do JSON
extracted_data = extract_items(json_data)

# Download stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# Preparar dados para o modelo TF-IDF
notes = list(extracted_data.values())
sentences = [preprocess(note) for note in notes]
dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]
tfidf_model = TfidfModel(corpus_bow, normalize=True)
index_tfidf = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

# Preparar dados para o modelo Word2Vec
model_w2v = Word2Vec.load("dre_w2v.model").wv
model_w2v.init_sims(replace=True)

def preprocess_w2v(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

# Preparar dados para o modelo Word2Vec
sentences_w2v = [preprocess_w2v(note) for note in notes]
doc_index_w2v = WmdSimilarity(sentences_w2v, model_w2v, num_best=10)

# Preparar dados para o modelo Doc2Vec
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
model_d2v = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)

# Preparar dados para o Universal Sentence Encoder (USE)
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

# Consulta
query = "leis de emigração e políticas estrangeiras"
query_tokens = preprocess(query)
query_bow = dictionary.doc2bow(query_tokens)
tfidf_query = tfidf_model[query_bow]

# Calcular similaridade com o modelo TF-IDF
sims_tfidf = index_tfidf[tfidf_query]
sims_ordered_tfidf = sorted(enumerate(sims_tfidf), key= lambda item: item[1], reverse = True)
index_tfidf, similarity_tfidf = sims_ordered_tfidf[0]
max_sim_id_tfidf = list(extracted_data.keys())[index_tfidf]
max_sim_value_tfidf = list(extracted_data.values())[index_tfidf]

# Calcular similaridade com o modelo Word2Vec
sims_w2v = doc_index_w2v[query_tokens]
max_sim_note_w2v = max(sims_w2v, key=lambda x: x[1])
max_sim_index_w2v = sims_w2v.index(max_sim_note_w2v)
max_sim_id_w2v = list(extracted_data.keys())[max_sim_index_w2v]
max_sim_value_w2v = list(extracted_data.values())[max_sim_index_w2v]

# Calcular similaridade com o modelo Doc2Vec
query_vector_d2v = model_d2v.infer_vector(query_tokens)
sims_d2v = model_d2v.docvecs.most_similar([query_vector_d2v], topn=1)
max_sim_id_d2v = list(extracted_data.keys())[sims_d2v[0][0]]
max_sim_value_d2v = list(extracted_data.values())[sims_d2v[0][0]]
max_similarity_d2v = sims_d2v[0][1]

# Calcular a representação vetorial do tema de consulta usando o Universal Sentence Encoder
query_vector_use = embed([query])[0]

# Calcular a representação vetorial de todas as notas usando o Universal Sentence Encoder
notes_vectors_use = embed(notes)

# Calcular similaridade de cosseno entre o tema de consulta e todas as notas usando o Universal Sentence Encoder
similarities_use = np.dot(query_vector_use, notes_vectors_use.T)

# Encontrar a nota mais semelhante usando o Universal Sentence Encoder
max_sim_index_use = np.argmax(similarities_use)
max_sim_value_use = np.max(similarities_use)
max_sim_id_use = list(extracted_data.keys())[max_sim_index_use]
max_sim_note_use = list(extracted_data.values())[max_sim_index_use]

# Imprimir resultados para o modelo TF-IDF
print("Modelo TF-IDF:")
print("ID:", max_sim_id_tfidf)
print("Nota:", max_sim_value_tfidf)
print("Similaridade:", similarity_tfidf)

# Imprimir resultados para o modelo Word2Vec
print("\nModelo Word2Vec:")
print("ID:", max_sim_id_w2v)
print("Nota:", max_sim_value_w2v)
print("Similaridade:", max_sim_note_w2v[1])

# Imprimir resultados para o modelo Doc2Vec
print("\nModelo Doc2Vec:")
print("ID:", max_sim_id_d2v)
print("Nota:", max_sim_value_d2v)
print("Similaridade:", max_similarity_d2v)

# Imprimir resultados para o Universal Sentence Encoder
print("\nModelo Universal Sentence Encoder:")
print("ID:", max_sim_id_use)
print("Nota:", max_sim_note_use)
print("Similaridade:", max_sim_value_use)
