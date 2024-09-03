import streamlit as st
import sqlite3

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def register_page():
    st.title("Criar Novo Usuário")
    
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Criar"):
        if username and password:
            register_user(username, password)
            st.success("Usuário criado com sucesso!")
            st.session_state['page'] = 'login'
        else:
            st.error("Por favor, preencha todos os campos.")
