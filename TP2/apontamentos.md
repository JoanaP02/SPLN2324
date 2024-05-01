#  Trabalho prático #

- Ver diferentes métodos e a forma como escala cada um (BERT, word embeddings (Word2Vec, GloVe))
- Possível usar várias bibliotecas
- Usar a base da aula mas explorar mais

sql light 3

meter informações a base de dados e fazer questoes

O trabalho de spln vai ser divido em 3 fases.

A primeira fase consiste em pegar num ficheiro JSON que tem as notas e os ids (meter em um txt)
e ao passar um tema-> procurar a nota e o id onde a nota se relaciona mais com o tema (já usamos TFIDF e WMD, BERT, procurar outras soluções)

A segunda fase consiste em analisar o csv dado, traduzir o id encontrado na primeira fase, no id correspondente na base de dados. Procurar na base de dados o texto associado aquele id. (Problema: o ficheira e mt gande)
O CSV é para transformar o id do JSON para o da base de dados


A terceira fase recebe o texto obtido na segunda fase e fazer question answering -> avaliar os modelos e escolher o melhor e ver as perguntas mais pertinentes

