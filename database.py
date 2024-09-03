import sqlite3

def create_db():
    # Conecte ao banco de dados (ou crie um novo se não existir)
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    # Crie a tabela de tarefas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        descricao TEXT NOT NULL,
        data DATE NOT NULL,
        hora TEXT NOT NULL,
        concluida BOOLEAN NOT NULL DEFAULT 0,
        data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        hora_adicao TEXT DEFAULT CURRENT_TIME
    )
    ''')

    conn.commit()
    conn.close()

def adicionar_tarefa(usuario, descricao, data, hora):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tarefas (usuario, descricao, data, hora)
    VALUES (?, ?, ?, ?)
    ''', (usuario, descricao, data, hora))

    conn.commit()
    conn.close()

def excluir_tarefas(usuario, id_inicial, id_final):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM tarefas
    WHERE usuario = ? AND id BETWEEN ? AND ?
    ''', (usuario, id_inicial, id_final))

    conn.commit()
    conn.close()

def editar_tarefa(usuario, id_tarefa, nova_descricao, nova_data, nova_hora):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE tarefas
    SET descricao = ?, data = ?, hora = ?
    WHERE usuario = ? AND id = ?
    ''', (nova_descricao, nova_data, nova_hora, usuario, id_tarefa))

    conn.commit()
    conn.close()

def obter_tarefas(usuario):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, descricao, data, hora, concluida, data_adicao, hora_adicao
    FROM tarefas
    WHERE usuario = ?
    ''', (usuario,))
    
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas
