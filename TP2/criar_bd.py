import sqlite3

def create_database():
    conn = sqlite3.connect('dre_database.db')
    cursor = conn.cursor()
    
    # Verificar se a tabela já existe e, se existir, eliminá-la
    cursor.execute('''
    DROP TABLE IF EXISTS dreapp_documenttext
    ''')

    # Criar a tabela dreapp_documenttext
    cursor.execute('''
    CREATE TABLE dreapp_documenttext (
        document_id INTEGER PRIMARY KEY,
        text TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_data_from_sql():
    conn = sqlite3.connect('dre_database.db')
    cursor = conn.cursor()
    
    # Ler o ficheiro SQL linha por linha e inserir dados
    with open('dados/2024-04-07-DRE_dump.sql', 'r', encoding='utf-8') as file:
        statement = ""
        for line in file:
            statement += line
            if line.strip().endswith(');'):
                if "INSERT INTO public.dreapp_documenttext VALUES" in statement:
                    # Remover o prefixo para facilitar a extração dos dados
                    statement = statement.replace("INSERT INTO public.dreapp_documenttext VALUES (", "")
                    
                    # Split pelo caractere vírgula
                    parts = statement.split(", ")
                    
                    # Extração dos elementos desejados
                    document_id = int(parts[1].strip())  # Certifique-se de converter para inteiro
                    text = ", ".join(parts[4:]).strip().strip("'")
                    
                    # Imprimir para verificação
                    #print("document_id:", document_id)
                    #print("text:", text[:100], "...")  # Mostrar apenas o início do texto para verificar
                    
                    # Inserir na base de dados
                    cursor.execute('INSERT INTO dreapp_documenttext (document_id, text) VALUES (?, ?)', (document_id, text))
                
                # Resetar o statement para a próxima linha
                statement = ""
    
    conn.commit()
    conn.close()

create_database()
insert_data_from_sql()
