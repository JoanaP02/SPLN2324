import os
import ijson
import nltk
import pickle
from gensim.utils import tokenize

def extract_items(json_file_path):
    extracted_data = {}
    with open(json_file_path, 'r', encoding="utf8") as json_data:
        for item in ijson.items(json_data, 'item'):
            extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

def save_extracted_data():
    # Ler o arquivo JSON
    filename = "dados/DRE_small.json"
    print("A ler o ficheiro JSON item a item...")
    extracted_data = extract_items(filename)

    # Save extracted_data to a pickle file
    print("A guardar os dados extraídos num ficheiro pickle...")
    with open('dados/extracted_data.pkl', 'wb') as f:
        pickle.dump(extracted_data, f)

def preprocess(line, stopwords):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

# TF-IDF
def create_tfidf_model(sentences):
    from gensim.corpora import Dictionary
    from gensim.models import TfidfModel
    from gensim.similarities import SparseMatrixSimilarity
    # Preparar dados para o modelo TF-IDF
    print("Preparando modelo TF-IDF...")
    dictionary = Dictionary(sentences)
    corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]
    tfidf_model = TfidfModel(corpus_bow, normalize=True)
    index_tfidf = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))
    # create folder if not exists
    if not os.path.exists("models/tfidf"):
        os.makedirs("models/tfidf")
    # save dictionary
    dictionary.save("models/tfidf/dictionary.dict")
    # save model
    tfidf_model.save("models/tfidf/tfidf.model")
    # save index_tfidf
    index_tfidf.save("models/tfidf/index_tfidf.index")

# Word2Vec Model
def create_word2vec_model(sentences):
    from gensim.models import Word2Vec
    model = Word2Vec(sentences, min_count=2, epochs=20, vector_size=300)
    # create folder if not exists
    if not os.path.exists("models/w2v"):
        os.makedirs("models/w2v")
    model.save("models/w2v/dre_w2v.model")

# Word2Vec Index
def create_word2vec_index(sentences):
    from gensim.models import Word2Vec
    from gensim.similarities import WmdSimilarity
    # Preparar dados para o modelo Word2Vec
    print("Preparando modelo Word2Vec...")
    model_w2v = Word2Vec.load("models/w2v/dre_w2v.model").wv
    model_w2v.init_sims(replace=True)
    doc_index_w2v = WmdSimilarity(sentences, model_w2v, num_best=10)
    doc_index_w2v.save("models/w2v/doc_index_w2v.index")

# Bert
def create_bert_model():
    import torch
    from transformers import pipeline
    print("Carregando modelo SentenceTransformer BERT...")
    pipe = pipeline('feature-extraction', model='neuralmind/bert-base-portuguese-cased', device=0 if torch.cuda.is_available() else -1, return_tensors=True)
    # Load extracted_data from a pickle file
    print("Carregando dados extraídos do arquivo pickle...")
    with open('dados/extracted_data.pkl', 'rb') as f:
        extracted_data = pickle.load(f)
    notes = list(extracted_data.values())
    notes_embeddings = [pipe(note) for note in notes]
    # save notes_embeddings
    with open('models/bert/notes_embeddings.pkl', 'wb') as f:
        pickle.dump(notes_embeddings, f)

def main():
    # Carregar stopwords
    stopwords = nltk.corpus.stopwords.words('portuguese')

    # Abrir extracted_data do arquivo pickle
    print("Carregando dados extraídos do arquivo pickle...")
    with open('dados/extracted_data.pkl', 'rb') as f:
        extracted_data = pickle.load(f)

    # Preparar dados para o modelo
    print("Preparando dados para o modelo...")
    notes = list(extracted_data.values())
    sentences = [preprocess(note, stopwords) for note in notes]
    return sentences