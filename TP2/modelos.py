import os
import ijson
import nltk
from gensim.utils import tokenize

def extract_items(json_data):
    extracted_data = {}
    for item in ijson.items(json_data, 'item'):
        extracted_data[str(item["claint"])] = item["notes"]
    return extracted_data

def preprocess(line, stopwords):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

# TF-IDF
def create_tfidf_model():
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
    # save model
    tfidf_model.save("models/tfidf/tfidf.model")
    # save index_tfidf
    index_tfidf.save("models/tfidf/index_tfidf.index")

# Word2Vec
def create_word2vec_model():
    from gensim.models import Word2Vec
    from gensim.similarities import WmdSimilarity
    # Preparar dados para o modelo Word2Vec
    print("Preparando modelo Word2Vec...")
    model_w2v = Word2Vec.load("models/dre_w2v.model").wv
    model_w2v.init_sims(replace=True)
    doc_index_w2v = WmdSimilarity(sentences, model_w2v, num_best=10)

# Bert
def create_bert_model():
    pass

# Carregar stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# Ler o arquivo JSON
filename = "dados/DRE_large.json"
print("A ler o ficheiro JSON item a item...")
extracted_data = extract_items(filename)

# Preparar dados para o modelo
print("Preparando dados para o modelo...")
notes = list(extracted_data.values())
sentences = [preprocess(note, stopwords) for note in notes]
