# Relatório de Desenvolvimento do Projeto

## Introdução

Este relatório descreve o desenvolvimento de um projeto que integra processamento de linguagem natural para responder a consultas e encontrar textos relevantes numa base de dados. O projeto utiliza diversos modelos para calcular similaridades, mapear IDs e aplicar modelos de question answering (QA).

## Etapas do Desenvolvimento

### 1. Preparação dos Dados

#### Leitura e Extração dos Dados

O primeiro passo foi ler e extrair dados de um ficheiro JSON contendo várias informaçẽs de diferentes documentos. Utilizámos funções para ler o ficheiro e extrair os dados relevantes para processamento posterior. Os dados pertinentes do JSON foram armazenados num dicionário, onde a chave é o ID do documento e o valor é a nota correspondente.

#### Preprocessamento dos Dados

Os dados extraídos foram preprocessados para tokenização e remoção de palavras irrelevantes (stopwords). Isto foi necessário para garantir que os dados estivessem num formato adequado para serem processados pelos modelos de machine learning.

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

O modelo BERT foi opcionalmente carregado para calcular similaridades de forma mais avançada, utilizando embeddings contextuais. Devido ao seu desempenho mais lento, foi adicionada a opção de ativar ou desativar o uso do BERT conforme necessário.

### 3. Cálculo de Similaridades

As similaridades entre a consulta e as notas foram calculadas utilizando os modelos preparados. Cada modelo produziu uma lista de similaridades ordenadas, e a nota com a maior similaridade foi selecionada, retornando o ID da mesma.

### 4. Mapeamento de IDs e Consulta do Texto

O ID calculado anteriormente foi mapeado para um ID interno, que corresponde ao da base de dados, usando um ficheiro CSV de mapeamento. Em seguida, com esse ID mapeado, foi possível consultar o texto referente ao documento na base de dados.

### 5. Aplicação de Modelos de QA

Diversos modelos de QA foram aplicados ao texto selecionado para responder a várias perguntas. As perguntas variaram desde questões simples sobre o conteúdo do texto até perguntas mais complexas sobre detalhes específicos.

### 6. Escrita dos Resultados

Os resultados foram escritos num ficheiro Markdown para melhor visualização. Isto incluiu a exibição do melhor modelo selecionado, o texto relevante encontrado e as respostas às perguntas feitas aos modelos de QA.

### Problemas e Soluções

#### Manipulação de Grandes Ficheiros

Encontrámos problemas ao manipular ficheiros SQL grandes. A solução foi ler o ficheiro linha a linha, processando e armazenando os dados de forma incremental para evitar sobrecarga de memória. Para isso, utilizámos um método que verifica se a linha contém dados relevantes e, em seguida, processa esses dados de forma incremental. O statement vai sendo acumulado até encontrar o delimitador `);`, indicando o final de um comando SQL completo. Neste ponto, os dados são extraídos, utilizando apenas o segundo ID e o texto, que são então inseridos na base de dados. Depois, o statement é redefinido para vazio, libertando memória.

#### Problemas de Tipo de Dados

Outro problema encontrado foi a incompatibilidade de tipos de dados ao consultar textos na base de dados. Garantimos que os IDs fossem convertidos para o tipo int nativo do Python antes de serem usados nas consultas SQL.

#### Desempenho do Modelo BERT

O modelo BERT apresentou um desempenho mais lento. Para mitigar isso, adicionámos a opção de ativar ou desativar o uso do modelo BERT conforme necessário.

### Conclusão

O projeto foi bem-sucedido em integrar diferentes modelos de machine learning para encontrar textos relevantes e aplicar question answering. As técnicas de manipulação de grandes ficheiros e conversão de tipos de dados garantiram a eficiência e robustez do sistema.
