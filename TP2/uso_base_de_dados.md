# Verificar a Base de Dados SQLite

## Passos para Verificar a Base de Dados

### 1. Abrir um terminal.

### 2. Navegue até o diretório onde a base de dados `dre_database.db` foi criada.

```bash
cd /SPLN2334/TP2
```

### 3. Inicie o cliente `sqlite3` com a base de dados:

```bash
sqlite3 dre_database.db
```
### 4. Execute os seguintes comandos no prompt `sqlite3` para verificar a tabela e os dados:

#### a. Listar as tabelas na base de dados:

```sql
.tables
```

#### b. Verificar a estrutura da tabela `dreapp_documenttext`:

```sql
.schema dreapp_documenttext
```

#### c. Contar o número de linhas na tabela `dreapp_documenttext`:

```sql
SELECT COUNT(*) FROM dreapp_documenttext;
```

#### d. Selecionar algumas linhas para verificar os dados:

```sql
SELECT * FROM dreapp_documenttext LIMIT 10;
```

#### e. Selecionar linha com id = :

```sql
SELECT COUNT(*) FROM dreapp_documenttext WHERE document_id = 606642;
```

### 5. Sair do cliente `sqlite3`:

```sql
.quit
```
