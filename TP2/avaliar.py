import psycopg2
import nltk
from gensim.utils import tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import ijson
from transformers import pipeline

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

# Função para chamar SQL e obter o texto associado ao ID
def chamarSQL(id):
    conn = psycopg2.connect("dbname=mydb user=afonsoni")
    cur = conn.cursor()
    cena = ""
    cur.execute(f'SELECT text FROM dreapp_documenttext WHERE document_id = {id};')
    sel = cur.fetchone()
    if sel is not None:
        cena = sel[0]
    return cena

# Carregar o arquivo de mapeamento
def load_mapping(mapping_file):
    dic = {}
    with open(mapping_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dic[row[0]] = row[1]
    return dic

# Carregar os dados e o modelo de pré-processamento
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# Carregar os dados do JSON
json_filename = "DRE_small.json"
json_data = read_json_file(json_filename)
extracted_data = extract_items(json_data)
notes = list(extracted_data.values())
sentences = [preprocess(note) for note in notes]

# Carregar o mapeamento de IDs
mapping_file = "id_mapping__.csv"
id_mapping = load_mapping(mapping_file)

# Obter o ID mapeado (exemplo)
original_id = "100111"  # Exemplo de ID original
mapped_id = id_mapping.get(original_id)

# Obter o texto correspondente ao ID mapeado
if mapped_id:
    context = chamarSQL(mapped_id)
else:
    context = None

# Verificar se o contexto foi encontrado
if context:
    print("Contexto obtido com sucesso.")
else:
    print("ID não encontrado no mapeamento ou na base de dados.")

# Parte 3: Question Answering

# Função para aplicar QA usando um modelo específico
def apply_qa_model(model_name, context, question):
    qa_pipeline = pipeline('question-answering', model=model_name)
    result = qa_pipeline(question=question, context=context)
    return result['answer']

# Função para avaliar múltiplos modelos
def evaluate_models(context, questions):
    models_to_evaluate = [
        "distilbert-base-cased-distilled-squad",
        "bert-large-uncased-whole-word-masking-finetuned-squad",
        "roberta-base-squad2"
    ]

    evaluation_results = {}
    for model in models_to_evaluate:
        answers = [apply_qa_model(model, context, question) for question in questions]
        evaluation_results[model] = answers

    return evaluation_results

# Definir perguntas de exemplo
questions = [
    "Qual é o objetivo principal do documento?",
    "Quem emitiu o documento?",
    "Qual é a data do documento?"
]

# Avaliar modelos se o contexto foi encontrado
if context:
    evaluation_results = evaluate_models(context, questions)

    # Imprimir resultados para comparação
    for model, answers in evaluation_results.items():
        print(f"Results for {model}:")
        for question, answer in zip(questions, answers):
            print(f"Q: {question}\nA: {answer}\n")
else:
    print("Nenhum contexto encontrado para avaliação.")
