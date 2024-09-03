import streamlit as st
import sqlite3

def authenticate_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        return user is not None
    except sqlite3.OperationalError as e:
        st.error(f"Erro no banco de dados: {e}")
        return False

def login_page():
    st.title("Login da Agenda")
    
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if not username or not password:
            st.error("Por favor, preencha todos os campos.")
        elif authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['page'] = 'main'
        else:
            st.error("Nome de usuário ou senha incorretos")
    
    if st.button("Esqueci a Senha"):
        st.session_state['page'] = 'reset_password'
    
    if st.button("Criar Novo Usuário"):
        st.session_state['page'] = 'register'

