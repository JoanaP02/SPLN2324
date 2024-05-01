from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
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

# Download stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

def preprocess(line):
    line = line.lower()
    tokens = tokenize(line)
    tokens = [token for token in tokens if token not in stopwords]
    return list(tokens)

notes = list(extracted_data.values())

sentences = [preprocess(note) for note in notes]

dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

tfidf_model = TfidfModel(corpus_bow, normalize=True)

index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

query = "leis de emigração e políticas estrangeiras"
query_tokens = preprocess(query)
query_bow = dictionary.doc2bow(query_tokens)
tfidf_query = tfidf_model[query_bow]

# Calculate similarity between the query and the notes
sims = index[tfidf_query]

sims_ordered = sorted(enumerate(sims), key= lambda item: item[1], reverse = True)

# print(sims_ordered[0])
# print("ID:", extracted_data.keys())[sims_ordered[0][0]]
# print("Nota:", extracted_data.values()[sims_ordered[0][0]])
# print("Similaridade:", sims_ordered[0][1])

index, similarity = sims_ordered[0]

max_sim_id = list(extracted_data.keys())[index]
max_sim_value = list(extracted_data.values())[index]

print("ID:", max_sim_id, "\nNota:", max_sim_value, "\nSimilaridade:", similarity)

 for index, sim in sims_ordered[:5]:
     print(sim)
     print(notes[index])

