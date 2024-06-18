import sqlite3
import pandas as pd
from gensim.models import TfidfModel, Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from gensim.utils import tokenize
from transformers import pipeline
import nltk
import ijson

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

def get_text_by_id(document_id):
    conn = sqlite3.connect('dre_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT text FROM dreapp_documenttext WHERE document_id=?', (document_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None

def load_id_mapping(csv_file):
    return pd.read_csv(csv_file, header=None, names=['document_id', 'external_id'])

def convert_id(external_id, id_mapping):
    record = id_mapping[id_mapping['external_id'] == external_id]
    if not record.empty:
        return record['document_id'].values[0]
    return None

def apply_qa_model(model_name, context, question):
    qa_pipeline = pipeline('question-answering', model=model_name)
    result = qa_pipeline(question=question, context=context)
    return result['answer']

def write_results_to_file(filename, results):
    with open(filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')

# Carregar stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# Parâmetro para ativar ou desativar BERT
use_bert = True # Defina como True para usar BERT

# Ler o arquivo JSON
filename = "dados/DRE_small.json"
json_data = read_json_file(filename)

# Extrair dados do JSON
print("Extraindo dados do JSON...")
extracted_data = extract_items(json_data)

# Preparar dados para o modelo
print("Preparando dados para o modelo...")
notes = list(extracted_data.values())
sentences = [preprocess(note) for note in notes]

# Preparar dados para o modelo TF-IDF
print("Preparando modelo TF-IDF...")
dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]
tfidf_model = TfidfModel(corpus_bow, normalize=True)
index_tfidf = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

# Preparar dados para o modelo Word2Vec
print("Preparando modelo Word2Vec...")
model_w2v = Word2Vec.load("models/dre_w2v.model").wv
model_w2v.init_sims(replace=True)
doc_index_w2v = WmdSimilarity(sentences, model_w2v, num_best=10)

# Carregar modelo SentenceTransformer
if use_bert:
    print("Carregando modelo SentenceTransformer BERT...")
    model_bert = SentenceTransformer('neuralmind/bert-base-portuguese-cased')

# Query
query = "Comida para animais de estimação"
query_tokens = preprocess(query)
query_bow = dictionary.doc2bow(query_tokens)

# Calcular similaridade com o modelo TF-IDF
print("Calculando similaridade com o modelo TF-IDF...")
tfidf_query = tfidf_model[query_bow]
sims_tfidf = index_tfidf[tfidf_query]
sims_tfidf_sorted = sorted(enumerate(sims_tfidf), key=lambda x: x[1], reverse=True)
max_sim_index_tfidf = sims_tfidf_sorted[0][0]
max_sim_id_tfidf = list(extracted_data.keys())[max_sim_index_tfidf]
max_sim_value_tfidf = list(extracted_data.values())[max_sim_index_tfidf]
max_sim_tfidf = sims_tfidf_sorted[0][1]

# Calcular similaridade com o modelo Word2Vec
print("Calculando similaridade com o modelo Word2Vec...")
sims_w2v = doc_index_w2v[query_tokens]
sims_w2v_sorted = sorted(sims_w2v, key=lambda x: x[1], reverse=True)
max_sim_index_w2v = sims_w2v_sorted[0][0]
max_sim_id_w2v = list(extracted_data.keys())[max_sim_index_w2v]
max_sim_value_w2v = list(extracted_data.values())[max_sim_index_w2v]
max_sim_w2v = sims_w2v_sorted[0][1]

# Calcular similaridade com o modelo SentenceTransformer
if use_bert:
    print("Calculando similaridade com o modelo SentenceTransformer BERT...")
    query_embedding = model_bert.encode(query)
    notes_embeddings = [model_bert.encode(note) for note in notes]
    similarities = cosine_similarity([query_embedding], notes_embeddings)
    most_similar_index_bert = similarities.argmax()
    most_similar_note_bert = notes[most_similar_index_bert]
    max_sim_id_bert = list(extracted_data.keys())[most_similar_index_bert]
    max_sim_value_bert = most_similar_note_bert
    max_sim_bert = similarities[0][most_similar_index_bert]

# Determinar a nota com a maior similaridade entre os três modelos
similarities_all = {
    'TF-IDF': max_sim_tfidf,
    'Word2Vec': max_sim_w2v,
}

if use_bert:
    similarities_all['BERT'] = max_sim_bert

best_model = max(similarities_all, key=similarities_all.get)

results = []

if best_model == 'TF-IDF':
    best_sim_id = max_sim_id_tfidf
    best_sim_value = max_sim_value_tfidf
elif best_model == 'Word2Vec':
    best_sim_id = max_sim_id_w2v
    best_sim_value = max_sim_value_w2v
else:
    best_sim_id = max_sim_id_bert
    best_sim_value = max_sim_value_bert

results.append(f"## Melhor modelo: {best_model}\n")
results.append(f"**ID:** {best_sim_id}\n")
results.append(f"**Nota:** {best_sim_value}\n")
results.append(f"**Similaridade:** {similarities_all[best_model]}\n")

# Adicionar a lógica de id_mapping
print("Carregando mapeamento de IDs...")
id_mapping = load_id_mapping('dados/id_mapping__.csv')
external_id = int(best_sim_id)  # ID externo obtido do modelo de similaridade
internal_id = int(convert_id(external_id, id_mapping))
results.append(f"**internal_id:** {internal_id}, **type:** {type(internal_id)}\n")

if internal_id:
    print(f"Buscando texto para o ID {internal_id} na base de dados...")
    # Buscar o texto na base de dados usando o ID mapeado
    text = get_text_by_id(internal_id)
    results.append(f"### Texto para o ID {internal_id}:\n{text}\n")
else:
    results.append(f"**ID {external_id} não encontrado no mapeamento.**\n")

# Lista de perguntas para o QA
questions = [
    "Qual é o principal objetivo mencionado no texto?",
    "Quais são as medidas principais mencionadas?",
    "Quem anunciou essas medidas?",
    "Quando foram anunciadas as medidas?",
    "Qual é a fonte das informações?",
    "Quais são os benefícios esperados?",
    "Há alguma crítica mencionada no texto?",
    "Quem são os beneficiários das medidas?",
    "Quais são os desafios mencionados?"
]

# Modelos de question answering
qa_models = [
    "lfcc/bert-portuguese-squad",
    "mrm8488/distilbert-multi-finedtuned-squad-pt",
    "ArthurBaia/xlm-roberta-base-squad-pt"
]

# Aplicar QA nos textos e avaliar
if text:
    print("Aplicando modelos de QA no texto...")
    results.append(f"### Texto Selecionado (ID {internal_id}):\n{text}\n")
    for question in questions:
        results.append(f"**Pergunta:** {question}\n")
        for model_name in qa_models:
            try:
                answer = apply_qa_model(model_name, text, question)
                results.append(f"**Modelo:** {model_name}\n**Resposta:** {answer}\n")
            except Exception as e:
                results.append(f"**Erro ao usar o modelo {model_name}:** {e}\n")

# Escrever resultados em um arquivo Markdown
print("Escrevendo resultados para o arquivo results.md...")
write_results_to_file('results.md', results)
print("Processo concluído.")