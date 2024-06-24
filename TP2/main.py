import os
import sqlite3
import pandas as pd
from gensim.models import TfidfModel, Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity, WmdSimilarity
from gensim.utils import tokenize
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
import nltk
import ijson
import pickle
import basedados

# Carregar stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

def read_json_file(filename):
    with open(filename, 'r', encoding="utf8") as file:
        for item in ijson.items(file, 'item'):
            yield item

def extract_items(filename):
    extracted_data = {}
    for item in read_json_file(filename):
        if 'claint' in item and 'notes' in item:
            extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

def preprocess(line):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

def get_text_by_id(document_id):
    conn = sqlite3.connect('dados/dre_database.db')
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

def create_database():
    basedados.create_database()
    basedados.insert_data_from_sql()

def create_models(models):
    import modelos
    # Existe extracted_data.pkl?
    if not os.path.exists('dados/extracted_data.pkl'):
        modelos.save_extracted_data()
    # If tfidf or word2vec in models, get sentences
    if 'tfidf' in models or 'word2vec' in models:
        sentences = modelos.main()
        if 'tfidf' in models:
            modelos.create_tfidf_model(sentences)
        if 'word2vec' in models:
            modelos.create_word2vec_model(sentences)
            modelos.create_word2vec_index(sentences)
    if 'bert' in models:
        modelos.create_bert_model()

def query(models, query):
    # Load extracted_data from a pickle file
    print("Carregando dados extraídos do arquivo pickle...")
    with open('dados/extracted_data.pkl', 'rb') as f:
        extracted_data = pickle.load(f)
    notes = list(extracted_data.values())

    # Query
    query_tokens = preprocess(query)

    # Ver que modelos foram chamados
    if 'tfidf' in models:
        # Check if the models are already created
        if not os.path.exists('models/tfidf/dictionary.dict'):
            print("Erro: modelo TF-IDF não encontrado. Crie os modelos primeiro.")
            return
        # Preparar dados para o modelo TF-IDF
        from gensim.models import TfidfModel
        from gensim.similarities import SparseMatrixSimilarity
        print("Preparando modelo TF-IDF...")
        dictionary = Dictionary.load('models/tfidf/dictionary.dict')
        tfidf_model = TfidfModel.load('models/tfidf/tfidf.model')
        index_tfidf = SparseMatrixSimilarity.load('models/tfidf/index_tfidf.index')
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

    if 'word2vec' in models:
        # Check if the models are already created
        if not os.path.exists('models/w2v/doc_index_w2v.index'):
            print("Erro: modelo Word2Vec não encontrado. Crie os modelos primeiro.")
            return
        # Preparar dados para o modelo Word2Vec
        from gensim.models import Word2Vec
        from gensim.similarities import WmdSimilarity
        print("Preparando modelo Word2Vec...")
        doc_index_w2v = WmdSimilarity.load("models/w2v/doc_index_w2v.index")

        # Calcular similaridade com o modelo Word2Vec
        print("Calculando similaridade com o modelo Word2Vec...")
        sims_w2v = doc_index_w2v[query_tokens]
        sims_w2v_sorted = sorted(sims_w2v, key=lambda x: x[1], reverse=True)
        max_sim_index_w2v = sims_w2v_sorted[0][0]
        max_sim_id_w2v = list(extracted_data.keys())[max_sim_index_w2v]
        max_sim_value_w2v = list(extracted_data.values())[max_sim_index_w2v]
        max_sim_w2v = sims_w2v_sorted[0][1]
    
    if 'bert' in models:
        # Carregar modelo SentenceTransformer
        print("Carregando modelo SentenceTransformer BERT...")
        pipeline = pipeline('feature-extraction', model='neuralmind/bert-base-portuguese-cased')

        # Calcular similaridade com o modelo SentenceTransformer
        print("Calculando similaridade com o modelo SentenceTransformer BERT...")
        # Load notes_embeddings from a pickle file
        with open('models/bert/notes_embeddings.pkl', 'rb') as f:
            notes_embeddings = pickle.load(f)
        # Query embedding
        query_embedding = pipeline(query)[0]
        similarities = torch.nn.functional.cosine_similarity(query_embedding, torch.stack(notes_embeddings))
        most_similar_index_bert = similarities.argmax()
        most_similar_note_bert = notes[most_similar_index_bert]
        max_sim_id_bert = list(extracted_data.keys())[most_similar_index_bert]
        max_sim_value_bert = most_similar_note_bert
        max_sim_bert = similarities[0][most_similar_index_bert]

    # Determinar a nota com a maior similaridade entre os três modelos
    similarities_all = {}
    if 'tfidf' in models:
        similarities_all['TF-IDF'] = max_sim_tfidf
    if 'word2vec' in models:
        similarities_all['Word2Vec'] = max_sim_w2v
    if 'bert' in models:
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

    results.append(f"## Resultados Finais: \n")
    results.append(f"### Melhor modelo: {best_model}\n")
    results.append(f"**ID:** {best_sim_id}\n")
    results.append(f"**Nota:** {best_sim_value}\n")
    results.append(f"**Similaridade:** {similarities_all[best_model]}\n")

    # Resultados dos outros modelos
    results.append("### Resultados dos outros modelos:\n")
    results.append(f"**TF-IDF:**\n**ID:** {max_sim_id_tfidf}, **Similaridade:** {max_sim_tfidf}\n")
    results.append(f"**Word2Vec:**\n**ID:** {max_sim_id_w2v}, **Similaridade:** {max_sim_w2v}\n")

    # Adicionar a lógica de id_mapping
    print("Carregando mapeamento de IDs...")
    id_mapping = load_id_mapping('dados/id_mapping__.csv')
    external_id = int(best_sim_id)  # ID externo obtido do modelo de similaridade
    internal_id = int(convert_id(external_id, id_mapping))

    if internal_id:
        print(f"Buscando texto para o ID {internal_id} na base de dados...")
        # Buscar o texto na base de dados usando o ID mapeado
        text = get_text_by_id(internal_id)
        print(text)
        results.append(f"### Texto Selecionado (ID {internal_id}):\n{text}\n")
    else:
        results.append(f"**ID {external_id} não encontrado no mapeamento.**\n")

    # Lista de perguntas para o QA
    questions = [
        "Qual é o principal objetivo?",
        "Qual a localidade?",
        "Quais são as medidas principais?",
        "Quais as entidades envolvidas?"
        "Quem anunciou essas medidas?",
        "Quando foram anunciadas as medidas?",
        "Qual é a fonte das informações?",
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
        results.append("### Perguntas e Respostas:\n")
        for question in questions:
            results.append(f"#### Pergunta: {question}\n")
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