# Uso

O programa pode ser executado a partir da linha de comando com vários argumentos opcionais.

## Argumentos

- `query`: A pergunta a ser processada.
- `--create_database`: Cria a base de dados.
- `--create_models`: Cria os modelos pré-treinados. Deve ser seguido por uma lista de modelos a serem criados.
- `--list_models` ou `-lm`: Lista os modelos disponíveis.
- `--models` ou `-m`: Especifica os modelos a serem utilizados para processar a pergunta. Se não especificado, todos os modelos disponíveis serão utilizados.

## Exemplos de Uso

### Listar Modelos Disponíveis

```bash
python prog.py --list_models
```

### Criar Base de Dados

```bash
python prog.py --create_database
```

### Criar Modelos

Para criar um ou mais modelos específicos:

```bash
python prog.py --create_models tfidf word2vec
```

### Processar uma Pergunta

Para processar uma pergunta utilizando os modelos especificados:

```bash
python prog.py "query aqui" --models tfidf word2vec
```

Se não especificar modelos, todos os modelos disponíveis serão usados por padrão:

```bash
python prog.py "query aqui"
```
