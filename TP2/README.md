# Relatório de Desenvolvimento do Projeto

[![](https://mermaid.ink/img/pako:eNp9VMFu2zAM_RVBpxVoLjvmUCCJE6DDCqyNsV58ISQmEWZLBiVjLYp-TLHDPiQ_NsqWHXsxejFIvkea5nvwm1ROo1zKQ-l-qxNQEHlWWCG-owkNwZdCpkhoJ3ZGndCQE9-8s4W8icQMAmxfAoEKxlnmt8n57_mP4xbPeHzWwBOaSmijmHX-IONG_T8Ia3IKvTf2yCMuOVRow2hQanrgpcsNIaR3bsikV6LICY3tWlra0JTv7rMdk7sqpwvOE_bsSH_9ieoC95VEWG-f8gu4563QKswJrD84qpASb28qUwKZ8LqBUjXlsOH5I6a8Fw4cDRr75dbow6U3ntErV5747CCsCyCUq0QFxpHwo_bUfZ89QF13x-MI-7MhI4mycdY3ZYiK9mGUNOALEy2IdU98XK3qujSq33zVJklQ7G8aw8eVgDQh9T5hHPzMn9Dtwh_BMbRidNgg4shki8Xd1EXXvkqUiVFm3cPEiTmu3MKE1ghzwKD5DBYNMLiI81mhx1b6jBOHfYbPAnGJiUuufcOUwQoTXzDQqz42A5cncl_pz4SJpoWVt5Ldzk7U_Nd4iw2FDCes2IpLDjXQr0IW9p150AS3f7VKLgM1eCvJNceTXB6g9Jw1tYaAmYEjQfVfdatNcJSK7_8ACQKk9g?type=png)](https://mermaid-live-editor.fly.dev/edit#pako:eNp9VMFu2zAM_RVBpxVoLjvmUCCJE6DDCqyNsV58ISQmEWZLBiVjLYp-TLHDPiQ_NsqWHXsxejFIvkea5nvwm1ROo1zKQ-l-qxNQEHlWWCG-owkNwZdCpkhoJ3ZGndCQE9-8s4W8icQMAmxfAoEKxlnmt8n57_mP4xbPeHzWwBOaSmijmHX-IONG_T8Ia3IKvTf2yCMuOVRow2hQanrgpcsNIaR3bsikV6LICY3tWlra0JTv7rMdk7sqpwvOE_bsSH_9ieoC95VEWG-f8gu4563QKswJrD84qpASb28qUwKZ8LqBUjXlsOH5I6a8Fw4cDRr75dbow6U3ntErV5747CCsCyCUq0QFxpHwo_bUfZ89QF13x-MI-7MhI4mycdY3ZYiK9mGUNOALEy2IdU98XK3qujSq33zVJklQ7G8aw8eVgDQh9T5hHPzMn9Dtwh_BMbRidNgg4shki8Xd1EXXvkqUiVFm3cPEiTmu3MKE1ghzwKD5DBYNMLiI81mhx1b6jBOHfYbPAnGJiUuufcOUwQoTXzDQqz42A5cncl_pz4SJpoWVt5Ldzk7U_Nd4iw2FDCes2IpLDjXQr0IW9p150AS3f7VKLgM1eCvJNceTXB6g9Jw1tYaAmYEjQfVfdatNcJSK7_8ACQKk9g)

## Introdução

Este relatório descreve o desenvolvimento de um projeto que integra processamento de linguagem natural para responder a consultas e encontrar textos relevantes numa base de dados. O projeto utiliza diversos modelos para calcular similaridades, mapear IDs e aplicar modelos de question answering (QA).

## Etapas do Desenvolvimento

### 1. Preparação dos Dados

#### Leitura e Extração dos Dados

O primeiro passo foi ler e extrair dados de um ficheiro JSON contendo várias informaçẽs de diferentes documentos. Foram utilizadas funções para ler o ficheiro e extrair os dados relevantes para processamento posterior. Os dados pertinentes do JSON foram armazenados num dicionário, onde a chave é o ID do documento e o valor é a nota correspondente.

#### Preprocessamento dos Dados

Os dados extraídos foram preprocessados para tokenização e remoção de palavras irrelevantes (stopwords). Isto foi necessário para garantir que os dados estivessem num formato adequado para serem processados pelos modelos.

### 2. Criação e Treino dos Modelos

#### Modelos Utilizados

Foram utilizados três modelos principais para calcular similaridades:

- **TF-IDF**
- **Word2Vec**
- **SentenceTransformer (BERT)**

#### Preparação do Modelo TF-IDF

O modelo TF-IDF foi utilizado para calcular a relevância dos termos em relação à consulta fornecida. Isto envolveu a criação de um dicionário de termos e a conversão dos dados para o formato bag-of-words.

#### Preparação do Modelo Word2Vec

O modelo Word2Vec foi carregado e treinado para calcular similaridades semânticas entre as notas e a consulta. Este modelo é especialmente útil para capturar relações semânticas entre palavras.

#### Preparação do Modelo SentenceTransformer

O modelo BERT foi opcionalmente carregado para calcular similaridades de forma mais avançada, utilizando embeddings contextuais.

### 3. Cálculo de Similaridades

As similaridades entre a consulta e as notas foram calculadas utilizando os modelos a cima descritos. Cada modelo produziu uma lista de similaridades ordenadas, e a nota com a maior similaridade foi selecionada, retornando o ID da mesma.

### 4. Mapeamento de IDs e Consulta do Texto

O ID calculado anteriormente foi mapeado para um ID interno, que corresponde ao da base de dados, usando um ficheiro CSV de mapeamento. Em seguida, com esse ID mapeado, foi possível consultar o texto referente ao documento na base de dados.

### 5. Aplicação de Modelos de QA

Diversos modelos de QA foram aplicados ao texto selecionado para responder a várias perguntas. As perguntas variaram desde questões simples sobre o conteúdo do texto até perguntas mais complexas sobre detalhes específicos.

### 6. Escrita dos Resultados

Os resultados foram escritos num ficheiro Markdown para melhor visualização. Isto incluiu a exibição do melhor modelo selecionado, o texto relevante encontrado e as respostas às perguntas feitas aos modelos de QA.

## Problemas e Soluções

### Manipulação de Grandes Ficheiros

Encontrámos problemas ao manipular ficheiros SQL grandes. A solução foi ler o ficheiro linha a linha, processando e armazenando os dados de forma incremental para evitar sobrecarga de memória. Para isso, utilizámos um método que verifica se a linha contém dados relevantes e, em seguida, processa esses dados de forma incremental. O statement vai sendo acumulado até encontrar o delimitador `);`, indicando o final de um comando SQL completo. Neste ponto, os dados são extraídos, utilizando apenas o segundo ID e o texto, que são então inseridos na base de dados. Depois, o statement é redefinido para vazio, libertando memória.

### Problemas de Tipo de Dados

Outro problema encontrado foi a incompatibilidade de tipos de dados ao consultar textos na base de dados. Garantimos que os IDs fossem convertidos para o tipo int nativo do Python antes de serem usados nas consultas SQL.

## Conclusão

O projeto foi bem-sucedido em integrar diferentes modelos para encontrar textos relevantes e aplicar question answering. As técnicas de manipulação de grandes ficheiros e conversão de tipos de dados garantiram a eficiência e robustez do sistema.

## Como utilizar

Antes de utilizar, é necessário criar a base de dados. Para isso basta utilizar o comando:

```bash
python basedados.py
```

Para verificar se a mesma foi criada e se está a funcionar como esperado é possível utilizadar os seguintes comandos:

### Passos para Verificar a Base de Dados

#### 1. Abrir um terminal.

#### 2. Navegar até o diretório onde a base de dados `dre_database.db` foi criada.

```bash
cd /SPLN2334/TP2/models
```

#### 3. Iniciar o cliente `sqlite3` com a base de dados:

```bash
sqlite3 dre_database.db
```

#### 4. Executar os seguintes comandos no prompt `sqlite3` para verificar a tabela e os dados:

##### a. Listar as tabelas na base de dados:

```sql
.tables
```

##### b. Verificar a estrutura da tabela `dreapp_documenttext`:

```sql
.schema dreapp_documenttext
```

##### c. Contar o número de linhas na tabela `dreapp_documenttext`:

```sql
SELECT COUNT(*) FROM dreapp_documenttext;
```

##### d. Selecionar algumas linhas para verificar os dados:

```sql
SELECT * FROM dreapp_documenttext LIMIT 10;
```

##### e. Selecionar linha com id = :

```sql
SELECT COUNT(*) FROM dreapp_documenttext WHERE document_id = 103313;
```

##### 5. Sair do cliente `sqlite3`:

```sql
.quit
```

### Correr o programa

Depois, deve seguir as instruções descritas da base de dados o programa pode ser executado através de diferentes argumentos:

#### Argumentos

- `query`: A pergunta a ser processada.
- `--create_database`: Cria a base de dados.
- `--create_models`: Cria os modelos pré-treinados. Deve ser seguido por uma lista de modelos a serem criados.
- `--list_models` ou `-lm`: Lista os modelos disponíveis.
- `--models` ou `-m`: Especifica os modelos a serem utilizados para processar a pergunta. Se não especificado, todos os modelos disponíveis serão utilizados.

#### Listar Modelos Disponíveis

```bash
python prog.py --list_models
```

#### Criar Base de Dados

```bash
python prog.py --create_database
```

#### Criar Modelos

Para criar um ou mais modelos específicos:

```bash
python prog.py --create_models tfidf word2vec
```

#### Processar uma Pergunta

Para processar uma pergunta utilizando os modelos especificados:

```bash
python prog.py "query aqui" --models tfidf word2vec
```

Se não especificar modelos, todos os modelos disponíveis serão usados por padrão:

```bash
python prog.py "query aqui"
```
