from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer, util

# Sentenças de exemplo
sentences = ["Esta é a primeira sentença.", "Esta é a segunda sentença."]
query = "Esta é uma consulta para encontrar similaridade."

# Inicializar o modelo BERT
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Codificar as sentenças e a consulta
sentence_embeddings = model.encode(sentences, convert_to_tensor=False)
query_embedding = model.encode(query, convert_to_tensor=False)

# Calcular a similaridade de cosseno entre a consulta e as sentenças
cosine_scores = util.cos_sim(query_embedding, sentence_embeddings)

# Calcular a média das similaridades de cosseno
average_similarity = sum(cosine_scores) / len(cosine_scores)

# Imprimir os resultados
for i, (sentence, score) in enumerate(zip(sentences, cosine_scores)):
    print("ID:", i + 1)
    print("Sentença:", sentence)
    print("Similaridade:", score.item())  # Utilize .item() para obter o valor escalar
    print()