import spacy

# Carregar o modelo de linguagem em português
nlp = spacy.load("pt_core_news_lg")

# Texto para processamento
text = "O Daniel e o André foram a Ponte de Lima a pé."
doc = nlp(text)

# Dicionário de tradução das partes do discurso
translate = {
    "ADJ": "adjetivo",
    "ADP": "preposição",
    "ADV": "advérbio",
    "AUX": "auxiliar",
    "CCONJ": "conjunção coordenativa",
    "DET": "determinante",
    "INTJ": "interjeição",
    "NOUN": "nome",
    "NUM": "número",
    "PART": "partícula",
    "PRON": "pronome",
    "PROPN": "nome próprio",
    "PUNCT": "pontuação",
    "SCONJ": "conjunção subordinativa",
    "SYM": "símbolo",
    "VERB": "verbo",
    "X": "outro"
}

# Função para gerar a tabela Markdown
def gerar_tabela(doc):
    tabela = "| Palavra | Tipo | Lema |\n|----|--------|----|\n"
    current_entity = []
    for token in doc:
        if token.ent_iob_ != "I" and current_entity:
            tabela += f"| {''.join(current_entity)} | nome próprio | {''.join(current_entity)} |\n"
            current_entity = []
        if token.ent_iob_ == "B":            
            current_entity.append(token.text_with_ws)
        elif token.ent_iob_ == "I":
            current_entity.append(token.text_with_ws)
        elif token.pos_ != "PUNCT":
            tabela += f"| {token.text} | {translate[token.pos_]} | {token.lemma_} |\n"
    if current_entity:
        tabela += f"| {''.join(current_entity)} | nome próprio | {''.join(current_entity)} |\n"
    return tabela

# Gerar e imprimir a tabela
tabela_resultado = gerar_tabela(doc)
print(tabela_resultado)
