import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.utils import tokenize
import ijson
import torch

print("Torch version:", torch.__version__)

print("Is CUDA enabled?", torch.cuda.is_available())

# Função para ler o arquivo JSON
def read_json_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
        json_data = file.read()
    return json_data

# Função para extrair itens do JSON
def extract_items(json_data):
    extracted_data = {}
    for item in ijson.items(json_data, 'item'):
        extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

# Função para pré-processar o texto
def preprocess(line):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

# Baixar stopwords para o idioma português
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# Ler o arquivo JSON
filename = "DRE_small.json"
print("Lendo arquivo JSON...")
json_data = read_json_file(filename)

# Extrair dados do JSON
print("Extraindo itens do JSON...")
extracted_data = extract_items(json_data)

# Obter as notas e tokenizá-las
print("Pré-processando as notas...")
notes = list(extracted_data.values())
sentences = [preprocess(note) for note in notes]

# Definir a consulta
#query = "leis de emigração e políticas estrangeiras"

query = "Regulamentação de tecnologias de informação e comunicação (TIC)"

'''
BERT
Aprova o plano global estratégico de racionalização e redução de custos com as TIC na Administração Pública, 
apresentado pelo Grupo de Projeto para as Tecnologias de Informação e Comunicação (GPTIC).                                         
Similaridade: 0.81124896  

Modelo TF-IDF:                                                                                                          
ID: 291530                                                                                                              
Nota: Aprova o plano global estratégico de racionalização e redução de custos com as TIC na Administração Pública, 
apresentado pelo Grupo de Projeto para as Tecnologias de Informação e Comunicação (GPTIC).                                   

Similaridade: 0.490551                                                                                                                                                                                                                          
Modelo Word2Vec:                                                                                                        
ID: 176640                                                                                                              
Nota: Nomeia representante da parte pública na assembçeia geral da MOVIJOVEM a licenciada Maria da Conceição Alves dos Santos Besa Ruão Pinto 
e suplente, nas faltas ou impedimentos daquela, o licenciado Mauro Renato Dias Xavier.            
Similaridade: 0.5439235769435347   
'''


# Carregar modelo SentenceTransformer específico para o português
print("Carregando modelo SentenceTransformer...")
model = SentenceTransformer('neuralmind/bert-base-portuguese-cased')

# Codificar a consulta em embeddings
print("Codificando a consulta em embeddings...")
query_embedding = model.encode(query) 

# Codificar as notas tokenizadas em embeddings
print("Codificando as notas em embeddings...")
notes_embeddings = [model.encode(note) for note in notes]  # Mantido como está
print(notes_embeddings)

# Calcular a similaridade entre a consulta e cada nota usando os embeddings
print("Calculando similaridades...")
similarities = cosine_similarity([query_embedding], notes_embeddings)

# Encontrar a nota com a maior similaridade com a consulta
print("Encontrando a nota mais similar à consulta...")
most_similar_index = similarities.argmax()
most_similar_note = notes[most_similar_index]

print("\nNota mais similar à consulta:")
print(most_similar_note)
print("Similaridade:", similarities[0][most_similar_index])
