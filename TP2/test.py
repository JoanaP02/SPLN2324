from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
import nltk 
import ijson

# Carregar o modelo BERT
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')

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
sentences = extract_items(json_data)

query = "leis de emigração e políticas estrangeiras"


# Codificar a consulta e as notas usando o modelo BERT
query_encoding = tokenizer(query, return_tensors="pt", padding=True, truncation=True)
query_embedding = model(**query_encoding).last_hidden_state.mean(dim=1)

note_embeddings = {}
for note_id, note_text in sentences.items():
    note_encoding = tokenizer(note_text, return_tensors="pt", padding=True, truncation=True)
    note_embedding = model(**note_encoding).last_hidden_state.mean(dim=1)
    note_embeddings[note_id] = note_embedding

# Calcular a similaridade de cosseno entre a consulta e as notas
similarities = {}
for note_id, note_embedding in note_embeddings.items():
    similarity = util.cos_sim(query_embedding, note_embedding)
    similarities[note_id] = similarity.item()

print(similarities)
# Encontrar a nota com a maior similaridade
max_similarity_note_id = max(similarities, key=similarities.get)
max_similarity_score = similarities[max_similarity_note_id]
max_similarity_note = sentences[max_similarity_note_id]

# Imprimir o resultado
print("ID da nota com maior similaridade:", max_similarity_note_id)
print("Nota com maior similaridade:", max_similarity_note)
print("Similaridade:", max_similarity_score)
