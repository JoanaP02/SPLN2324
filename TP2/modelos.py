from gensim.models import TfidfModel, Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from gensim.utils import tokenize
import nltk 
import ijson
import torch


def read_json_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
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
notes = list(extracted_data.values())
sentences = [preprocess(note) for note in notes]

# Preparar dados para o modelo TF-IDF
dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]
tfidf_model = TfidfModel(corpus_bow, normalize=True)
index_tfidf = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

# Preparar dados para o modelo Word2Vec
model_w2v = Word2Vec.load("dre_w2v.model").wv
model_w2v.init_sims(replace=True)
doc_index_w2v = WmdSimilarity(sentences, model_w2v, num_best=10)

# Query
#query = "leis de emigração e políticas estrangeiras"
query = "Comida para animais de estimação"
query_tokens = preprocess(query)
query_bow = dictionary.doc2bow(query_tokens)
tfidf_query = tfidf_model[query_bow]

# Calcular similaridade com o modelo TF-IDF
sims_tfidf = index_tfidf[tfidf_query]
sims_tfidf_sorted = sorted(enumerate(sims_tfidf), key=lambda x: x[1], reverse=True)

# Extrair o índice da nota com maior similaridade
max_sim_index_tfidf = sims_tfidf_sorted[0][0]

# Obter o ID da nota com maior similaridade
max_sim_id_tfidf = list(extracted_data.keys())[max_sim_index_tfidf]

# Obter o conteúdo da nota com maior similaridade
max_sim_value_tfidf = list(extracted_data.values())[max_sim_index_tfidf]

# Imprimir resultados para o modelo TF-IDF
print("\nModelo TF-IDF:")
print("ID:", max_sim_id_tfidf)
print("Nota:", max_sim_value_tfidf)
print("Similaridade:", sims_tfidf_sorted[0][1])


# Calcular similaridade com o modelo Word2Vec
sims_w2v = doc_index_w2v[query_tokens]
sims_w2v_sorted = sorted(sims_w2v, key=lambda x: x[1], reverse=True)

# Extrair o índice da nota com maior similaridade
max_sim_index_w2v = sims_w2v_sorted[0][0]

# Obter o ID da nota com maior similaridade
max_sim_id_w2v = list(extracted_data.keys())[max_sim_index_w2v]

# Obter o conteúdo da nota com maior similaridade
max_sim_value_w2v = list(extracted_data.values())[max_sim_index_w2v]

# Imprimir resultados para o modelo Word2Vec
print("\nModelo Word2Vec:")
print("ID:", max_sim_id_w2v)
print("Nota:", max_sim_value_w2v)
print("Similaridade:", sims_w2v_sorted[0][1])


'''
# Imprimir as 10 notas mais similares para o modelo TF-IDF
for i in range(10):
    index, sim = sims_tfidf_sorted[i]
    print("Similaridade:", sim)
    print("Nota:", notes[index])
    
# Imprimir as 10 notas mais similares para o modelo Word2Vec
for index, sim in sims_w2v_sorted[:10]:
    print(sim)
    print(notes[index])
'''

print("Carregando modelo SentenceTransformer...")
model = SentenceTransformer('neuralmind/bert-base-portuguese-cased')

# Codificar a consulta em embeddings
print("Codificando a consulta em embeddings...")
query_embedding = model.encode(query)

# Codificar as notas tokenizadas em embeddings
print("Codificando as notas em embeddings...")
notes_embeddings = [model.encode(note) for note in notes]

# Calcular a similaridade entre a consulta e cada nota usando os embeddings
similarities = cosine_similarity([query_embedding], notes_embeddings)

# Encontrar a nota com a maior similaridade com a consulta
most_similar_index = similarities.argmax()
most_similar_note = notes[most_similar_index]

print("\nModelo SentenceTransformer:")
print("ID:", most_similar_index)
print("Nota:", most_similar_note)
print("Similaridade:", similarities[0][most_similar_index])


# Resultados

'''
Modelo TF-IDF:
ID: 305570
Nota: ALTERA A PORTARIA NUMERO 575/93, DE 4 DE JUNHO (APROVA O REGULAMENTO DOS CONTROLOS VETERINÁRIOS E ZOOTÉCNICOS,
APLICÁVEIS AO COMERCIO INTRACOMUNITÁRIO DE ANIMAIS VIVOS E PRODUTOS ANIMAIS.
Similaridade: 0.45846555

Modelo Word2Vec:
ID: 274171
Nota: Estabelece o regime de importação de alimentos compostos para animais à base de cereais.
Similaridade: 0.5621504490290059
'''