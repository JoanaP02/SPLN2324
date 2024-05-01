from gensim.models import TfidfModel, Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from gensim.utils import tokenize
import nltk 
import ijson

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
