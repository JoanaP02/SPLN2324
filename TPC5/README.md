---
Título: TPC5
Data: 17 de março de 2024
Autor: Joana Pereira
UC: SPLN
---

## Resumo

O código carrega o modelo de processamento de linguagem natural "pt_core_news_lg" do spaCy e realiza o processamento de um texto em português. Em seguida, são identificadas as diferentes partes do discurso e é gerada uma tabela em Markdown com as palavras, os seus tipos e lemas respetivos.

## Dependências

Para correr o script, é necessário ter o **python3** instalado.

```sh
sudo apt install python3
```

A biblioteca spaCy:

```sh
pip install spacy
```

E o pacote pt_core_news_lg do spaCy:

```sh
python -m spacy download pt_core_news_lg
```

## Instruções de Execução

Para executar o script, deve-se correr o seguinte comando:

```sh
python3 parseTexto.py > resultado.md
```
