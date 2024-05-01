import tensorflow_hub as hub
import numpy as np

from gensim.models import TfidfModel, Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from gensim.utils import tokenize
import nltk 
import ijson

# #download the model to local so it can be used again and again
# !mkdir ../sentence_wise_email/module/module_useT
# # Download the module, and uncompress it to the destination folder. 
# !curl -L "https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed" | tar -zxvC ../sentence_wise_email/module/module_useT

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

# Carregar o Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

# Preprocessamento do tema de consulta
query = "leis de emigração e políticas estrangeiras"

# Preparar dados das notas
notes = list(extracted_data.values())

# Calcular a representação vetorial do tema de consulta
query_vector = embed([query])[0]

# Calcular a representação vetorial de todas as notas
notes_vectors = embed(notes)

# Calcular similaridade de cosseno entre o tema de consulta e todas as notas
similarities = np.dot(query_vector, notes_vectors.T)

# Encontrar a nota mais semelhante
max_sim_index_use = np.argmax(similarities)
max_sim_value_use = np.max(similarities)
max_sim_id_use = list(extracted_data.keys())[max_sim_index_use]
max_sim_note_use = list(extracted_data.values())[max_sim_index_use]

# Imprimir resultados para o modelo Universal Sentence Encoder
print("\nModelo Universal Sentence Encoder:")
print("ID:", max_sim_id_use)
print("Nota:", max_sim_note_use)
print("Similaridade:", max_sim_value_use)
