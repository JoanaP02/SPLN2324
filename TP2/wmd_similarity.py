from gensim.models import Word2Vec
from gensim.similarities import WmdSimilarity
from gensim.utils import tokenize
import nltk 

import ijson

def read_json_file(filename):
    with open(filename, 'r') as file:
        json_data = file.read()
    return json_data

# Ler o arquivo JSON
filename = "DRE_small.json"
json_data = read_json_file(filename)


# Extract the items from the JSON data and store them in a dictionary
def extract_items(json_data):
    extracted_data = {}
    for item in ijson.items(json_data, 'item'):
        extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

# Extract items and print the dictionary
extracted_data = extract_items(json_data)

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

model_w2v = Word2Vec.load("dre_w2v.model").wv
model_w2v.init_sims(replace=True)

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

# Extrair notas do dicionário
notes = list(extracted_data.values())

sentences = [preprocess(note) for note in notes]

#print(sentences)

doc_index = WmdSimilarity(sentences, model_w2v, num_best=10)

query = "leis de emigração e políticas estrangeiras"
query_tokens = preprocess(query)

# Calcular similaridade entre a consulta e as notas
sims = doc_index[query_tokens]

# Encontrar a nota mais semelhante
max_sim_note = max(sims, key=lambda x: x[1])

# Encontrar o ID da nota mais semelhante
max_sim_index = sims.index(max_sim_note)

# Imprimir ID, nota e valor da maior similaridade
max_sim_id = list(extracted_data.keys())[max_sim_index]
max_sim_value = list(extracted_data.values())[max_sim_index]
print("ID:", max_sim_id)
print("Nota:", max_sim_value)
print("Similaridade:", max_sim_note[1])
