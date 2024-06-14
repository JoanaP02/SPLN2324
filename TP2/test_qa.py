from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Função para aplicar QA usando um modelo específico
def apply_qa_model(model_name, context, question):
    qa_pipeline = pipeline('question-answering', model=model_name)
    result = qa_pipeline(question=question, context=context)
    return result['answer']

# Função para calcular a similaridade entre a resposta do modelo e a resposta esperada
def calculate_similarity(answer, expected_answer):
    vectorizer = CountVectorizer().fit_transform([answer, expected_answer])
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)
    return csim[0][1]

# Função para escrever resultados em um arquivo de texto
def write_results_to_file(filename, results):
    with open(filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')

def main():
    # Exemplos de textos do Diário da República
    texto_1 = """
    O Ministro da Educação anunciou hoje novas medidas para melhorar a qualidade do ensino nas escolas públicas.
    Entre as medidas estão o aumento do investimento em infraestrutura, a contratação de mais professores,
    e a modernização dos currículos escolares. O objetivo é garantir que todos os estudantes tenham acesso
    a uma educação de alta qualidade e estejam preparados para os desafios do futuro.
    """
    texto_2 = """
    A nova legislação de proteção ambiental foi aprovada pelo Parlamento. As novas leis incluem restrições
    sobre a emissão de poluentes industriais e promovem o uso de energias renováveis. Esta legislação visa
    reduzir a pegada de carbono do país e combater as mudanças climáticas.
    """
    texto_3 = """
    O Presidente da República promulgou a lei que estabelece o salário mínimo nacional. A nova lei aumenta
    o salário mínimo para garantir melhores condições de vida para os trabalhadores. Esta medida faz parte
    de um conjunto de políticas para promover a justiça social e a igualdade econômica.
    """

    # Conjunto de textos
    textos = [texto_1, texto_2, texto_3]

    # Definir perguntas e respostas esperadas para cada texto
    qa_pairs = [
        [
            ("Quem anunciou novas medidas para melhorar a qualidade do ensino?", "O Ministro da Educação"),
            ("Quais são algumas das medidas anunciadas?", "aumento do investimento em infraestrutura, a contratação de mais professores, e a modernização dos currículos escolares"),
            ("Qual é o objetivo das novas medidas?", "garantir que todos os estudantes tenham acesso a uma educação de alta qualidade e estejam preparados para os desafios do futuro")
        ],
        [
            ("Quem aprovou a nova legislação de proteção ambiental?", "o Parlamento"),
            ("O que incluem as novas leis?", "restrições sobre a emissão de poluentes industriais e promovem o uso de energias renováveis"),
            ("Qual é o objetivo da nova legislação?", "reduzir a pegada de carbono do país e combater as mudanças climáticas")
        ],
        [
            ("Quem promulgou a lei que estabelece o salário mínimo nacional?", "O Presidente da República"),
            ("O que faz a nova lei?", "aumenta o salário mínimo para garantir melhores condições de vida para os trabalhadores"),
            ("Qual é o objetivo das políticas?", "promover a justiça social e a igualdade econômica")
        ]
    ]

    # Modelos de question answering da TUGAAA
    models = [
        "lfcc/bert-portuguese-squad",
        "mrm8488/distilbert-multi-finedtuned-squad-pt",
        "ArthurBaia/xlm-roberta-base-squad-pt",
        "lfcc/bert-portuguese-squad2"
    ]

    # Lista para armazenar os resultados
    results = []

    # Aplicar question answering nos textos e avaliar
    for i, (texto, qa_pair) in enumerate(zip(textos, qa_pairs)):
        results.append(f"\nTexto {i+1}:\n{texto}\n")
        for model_name in models:
            results.append(f"Resultados para o modelo: {model_name}\n")
            total_score = 0
            for question, expected_answer in qa_pair:
                try:
                    answer = apply_qa_model(model_name, texto, question)
                    score = calculate_similarity(answer, expected_answer)
                    total_score += score
                    results.append(f"Q: {question}\nA: {answer}\nEsperado: {expected_answer}\nScore: {score:.2f}\n")
                except Exception as e:
                    results.append(f"Erro ao usar o modelo {model_name}: {e}\n")
            avg_score = total_score / len(qa_pair)
            results.append(f"Pontuação média para o modelo {model_name}: {avg_score:.2f}\n")

    # Escrever resultados em um arquivo de texto
    write_results_to_file('resultados_qa.txt', results)

if __name__ == "__main__":
    main()
