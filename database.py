import sqlite3

def connect_db():
    return sqlite3.connect('database.db')  # Substitua pelo caminho correto do seu banco de dados

def add_event(username, date, time, description):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO events (username, Date, Time, Description) VALUES (?, ?, ?, ?)',
              (username, date, time, description))
    conn.commit()
    conn.close()



def create_tables():
    conn = sqlite3.connect('database.db')  # Substitua pelo caminho correto do seu banco de dados
    c = conn.cursor()
    
    # Cria a tabela de eventos se não existir
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            Date TEXT NOT NULL,
            Time TEXT NOT NULL,
            Description TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Chame a função para criar as tabelas
create_tables()


# Função para criar uma conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Função para adicionar um evento
def add_event(username, date, time, description):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO events (username, Date, Time, Description) VALUES (?, ?, ?, ?)',
              (username, date, time, description))
    conn.commit()
    conn.close()

# Função para obter os eventos de um usuário
def get_events(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE username = ?', (username,))
    events = c.fetchall()
    conn.close()
    return [{"ID": event[0], "Date": event[2], "Time": event[3], "Description": event[4]} for event in events]

# Função para excluir um evento
def delete_event(username, event_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE ID = ? AND username = ?', (event_id, username))
    conn.commit()
    conn.close()

# Função para atualizar um evento
def update_event(username, event_id, new_date, new_time, new_description):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''UPDATE events
                 SET Date = ?, Time = ?, Description = ?
                 WHERE ID = ? AND username = ?''',
              (new_date, new_time, new_description, event_id, username))
    conn.commit()
    conn.close()
