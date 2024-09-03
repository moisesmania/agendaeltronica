import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, descricao TEXT, concluida BOOLEAN)''')
    conn.commit()
    conn.close()

def adicionar_tarefa(username, descricao):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO tarefas (username, descricao, concluida) VALUES (?, ?, ?)", (username, descricao, False))
    conn.commit()
    conn.close()

def excluir_tarefa(username, id_tarefa):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id=? AND username=?", (id_tarefa, username))
    conn.commit()
    conn.close()

def editar_tarefa(username, id_tarefa, nova_descricao):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE tarefas SET descricao=? WHERE id=? AND username=?", (nova_descricao, id_tarefa, username))
    conn.commit()
    conn.close()

def obter_tarefas(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tarefas WHERE username=?", (username,))
    tarefas = c.fetchall()
    conn.close()
    return tarefas
